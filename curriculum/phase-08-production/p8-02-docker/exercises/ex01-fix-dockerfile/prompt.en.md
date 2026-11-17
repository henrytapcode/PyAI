The `DOCKERFILE` string in `starter.py` builds a FastAPI service image, but it has **four bugs** that cause all four checks in the test suite to fail:

1. **Unpinned base image** (`test_base_image_pins_a_specific_tag` fails): future builds can silently pull a different Python release.
2. **Broken build-cache order** (`test_copies_requirements_before_installing_then_app_code` fails): any edit to application code invalidates the dependency installation step and forces a full reinstall.
3. **Bloated `pip` layer** (`test_pip_install_uses_no_cache_dir` fails): downloaded `.whl` package archives stay baked inside the image layer.
4. **Unreachable container port** (`test_cmd_uses_exec_form_and_binds_all_interfaces` fails): traffic forwarded from the host machine with `-p 8000:8000` is refused by the container.

Fix `DOCKERFILE` directly in `starter.py` so all four checks pass.

**Example**

```text
test_base_image_pins_a_specific_tag                       -> PASSED
test_copies_requirements_before_installing_then_app_code -> PASSED
test_pip_install_uses_no_cache_dir                       -> PASSED
test_cmd_uses_exec_form_and_binds_all_interfaces         -> PASSED
```

**Rules**
- Keep `DOCKERFILE` as a multi-line string inside `starter.py` (do not run `docker`).
- Keep `WORKDIR /app`, `EXPOSE 8000`, `requirements.txt` installation, and `uvicorn main:app` on port `8000` in JSON exec form.
- Resolve all four failing symptoms above so the image is reproducible, cache-friendly, lean, and reachable from the host.
