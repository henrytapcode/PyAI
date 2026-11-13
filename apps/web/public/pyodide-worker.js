/* Python in the browser: Pyodide runs inside this Web Worker so an infinite loop never
 * freezes the page (the app can terminate and restart the worker).
 * Messages in:  {type:"init"} | {type:"run", id, code} | {type:"test", id, code, tests} | {type:"trace", id, code}
 * Messages out: {type:"status", status} | {type:"ready", version} | {type:"stdout"|"stderr", id, text}
 *               | {type:"image", id, data} | {type:"done", id, ok, error} | {type:"result", id, result} | {type:"fatal", error}
 * "trace" answers with {type:"result", id, result} where result is tools/pyrunner/tracer.py's JSON.
 */
const PYODIDE_VERSION = "0.29.5";
const INDEX_URL = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;

let pyodide = null;
let readyPromise = null;
let currentId = null;

function post(msg) {
  self.postMessage(msg);
}

async function init() {
  if (readyPromise) return readyPromise;
  readyPromise = (async () => {
    post({ type: "status", status: "loading" });
    importScripts(`${INDEX_URL}pyodide.js`);
    pyodide = await self.loadPyodide({ indexURL: INDEX_URL });
    pyodide.setStdout({ batched: (text) => post({ type: "stdout", id: currentId, text: text + "\n" }) });
    pyodide.setStderr({ batched: (text) => post({ type: "stderr", id: currentId, text: text + "\n" }) });
    for (const name of ["runner", "tracer"]) {
      const src = await (await fetch(new URL(`pyrunner/${name}.py`, self.location.href))).text();
      pyodide.FS.writeFile(`/home/pyodide/pyai_${name}.py`, src);
    }
    await pyodide.runPythonAsync(`
import sys, builtins, ast, os, io, base64, json
sys.path.insert(0, "/home/pyodide")
import pyai_runner, pyai_tracer

def _no_input(prompt=""):
    raise RuntimeError("input() is not available in the browser editor. Assign a value directly, e.g. name = 'Lan'.")
builtins.input = _no_input

def _pyai_uses_matplotlib(code):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and any(
            a.name == "matplotlib" or a.name.startswith("matplotlib.") for a in node.names
        ):
            return True
        if isinstance(node, ast.ImportFrom) and node.module and (
            node.module == "matplotlib" or node.module.startswith("matplotlib.")
        ):
            return True
    return False

def _pyai_prepare_mpl():
    os.environ["MPLBACKEND"] = "Agg"
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.show = lambda *a, **k: None

def _pyai_collect_mpl_images():
    import matplotlib.pyplot as plt
    imgs = []
    try:
        for num in plt.get_fignums():
            fig = plt.figure(num)
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=100, bbox_inches="tight")
            b64 = base64.b64encode(buf.getvalue()).decode("ascii")
            imgs.append(f"data:image/png;base64,{b64}")
    finally:
        plt.close("all")
    return json.dumps(imgs)

def _pyai_close_mpl():
    import matplotlib.pyplot as plt
    plt.close("all")
`);
    post({ type: "ready", version: pyodide.version });
  })();
  try {
    await readyPromise;
  } catch (err) {
    readyPromise = null;
    post({ type: "fatal", error: String(err && err.message ? err.message : err) });
    throw err;
  }
  return readyPromise;
}

/** Keep only the learner's frames in a traceback (drop Pyodide internals). */
function cleanTraceback(message) {
  const lines = String(message).split("\n");
  const out = [];
  let skip = false;
  for (const line of lines) {
    if (/^\s+File "\/lib\//.test(line)) {
      skip = true;
      continue;
    }
    if (skip && /^\s{4}/.test(line)) continue;
    skip = false;
    out.push(line.replace('File "<exec>"', 'File "main.py"'));
  }
  return out.join("\n").trim();
}

async function loadImports(code) {
  try {
    await pyodide.loadPackagesFromImports(code, {
      messageCallback: (m) => post({ type: "stderr", id: currentId, text: `[packages] ${m}\n` }),
    });
  } catch (err) {
    // Unknown imports surface later as a normal ImportError.
  }
}

function usesMatplotlib(code) {
  if (!code || !/\bmatplotlib\b/.test(code)) return false;
  const fn = pyodide.globals.get("_pyai_uses_matplotlib");
  try {
    return Boolean(fn(code));
  } finally {
    fn.destroy();
  }
}

function prepareMpl() {
  pyodide.runPython("_pyai_prepare_mpl()");
}

function collectMplImages() {
  return JSON.parse(pyodide.runPython("_pyai_collect_mpl_images()"));
}

function closeMpl() {
  pyodide.runPython("_pyai_close_mpl()");
}

self.onmessage = async (event) => {
  const msg = event.data;
  try {
    if (msg.type === "init") {
      await init();
      return;
    }
    await init();
    currentId = msg.id;
    if (msg.type === "run") {
      await loadImports(msg.code);
      pyodide.runPython("pyai_runner.reset_state()");
      const hasMpl = usesMatplotlib(msg.code);
      if (hasMpl) prepareMpl();
      const globals = pyodide.globals.get("dict")();
      globals.set("__name__", "__main__");
      let runOk = true;
      let runError = null;
      try {
        await pyodide.runPythonAsync(msg.code, { globals, filename: "main.py" });
      } catch (err) {
        runOk = false;
        runError = cleanTraceback(err.message);
      } finally {
        if (hasMpl) {
          try {
            for (const data of collectMplImages()) {
              post({ type: "image", id: msg.id, data });
            }
          } catch (_imgErr) {
            // Keep figure export errors from suppressing the final "done" message.
          }
        }
        globals.destroy();
      }
      post({ type: "done", id: msg.id, ok: runOk, error: runError });
    } else if (msg.type === "test") {
      await loadImports(msg.code);
      if (msg.tests) await loadImports(msg.tests);
      const hasMpl = usesMatplotlib(msg.code) || usesMatplotlib(msg.tests);
      if (hasMpl) prepareMpl();
      const runTests = pyodide.globals.get("pyai_runner").run_tests_json;
      try {
        const json = runTests(msg.code, msg.tests);
        post({ type: "result", id: msg.id, result: JSON.parse(json) });
      } finally {
        runTests.destroy();
        if (hasMpl) closeMpl();
      }
    } else if (msg.type === "trace") {
      await loadImports(msg.code);
      pyodide.runPython("pyai_runner.reset_state()");
      const hasMpl = usesMatplotlib(msg.code);
      if (hasMpl) prepareMpl();
      const traceJson = pyodide.globals.get("pyai_tracer").trace_json;
      try {
        const json = traceJson(msg.code);
        post({ type: "result", id: msg.id, result: JSON.parse(json) });
      } finally {
        traceJson.destroy();
        if (hasMpl) closeMpl();
      }
    }
  } catch (err) {
    post({ type: "done", id: msg.id, ok: false, error: String(err && err.message ? err.message : err) });
  }
};
