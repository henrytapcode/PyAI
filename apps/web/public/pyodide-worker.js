/* Python in the browser: Pyodide runs inside this Web Worker so an infinite loop never
 * freezes the page (the app can terminate and restart the worker).
 * Messages in:  {type:"init"} | {type:"run", id, code} | {type:"test", id, code, tests} | {type:"trace", id, code}
 * Messages out: {type:"status", status} | {type:"ready", version} | {type:"stdout"|"stderr", id, text}
 *               | {type:"done", id, ok, error} | {type:"result", id, result} | {type:"fatal", error}
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
import sys, builtins
sys.path.insert(0, "/home/pyodide")
import pyai_runner, pyai_tracer

def _no_input(prompt=""):
    raise RuntimeError("input() is not available in the browser editor. Assign a value directly, e.g. name = 'Lan'.")
builtins.input = _no_input
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
      const globals = pyodide.globals.get("dict")();
      globals.set("__name__", "__main__");
      try {
        await pyodide.runPythonAsync(msg.code, { globals, filename: "main.py" });
        post({ type: "done", id: msg.id, ok: true, error: null });
      } catch (err) {
        post({ type: "done", id: msg.id, ok: false, error: cleanTraceback(err.message) });
      } finally {
        globals.destroy();
      }
    } else if (msg.type === "test") {
      await loadImports(msg.code);
      const runTests = pyodide.globals.get("pyai_runner").run_tests_json;
      const json = runTests(msg.code, msg.tests);
      runTests.destroy();
      post({ type: "result", id: msg.id, result: JSON.parse(json) });
    } else if (msg.type === "trace") {
      await loadImports(msg.code);
      pyodide.runPython("pyai_runner.reset_state()");
      const traceJson = pyodide.globals.get("pyai_tracer").trace_json;
      const json = traceJson(msg.code);
      traceJson.destroy();
      post({ type: "result", id: msg.id, result: JSON.parse(json) });
    }
  } catch (err) {
    post({ type: "done", id: msg.id, ok: false, error: String(err && err.message ? err.message : err) });
  }
};
