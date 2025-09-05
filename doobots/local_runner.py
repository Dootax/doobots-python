#!/usr/bin/env python3
import sys, json, importlib.util, traceback
import multiprocessing, queue
from doobots import Request, Response

TIMEOUT = 300  # seconds

def run_user(q, data, user_module):
    try:
        if not hasattr(user_module, "main"):
            q.put({"__error__": "no_main", "detail": "main(input) not found"})
            return

        result = user_module.main(Request(data))

        if isinstance(result, Response):
            q.put({"__result__": result.to_dict()})
        elif isinstance(result, dict):
            q.put({"__result__": result})
        else:
            q.put({"__error__": "invalid_return", "detail": "main deve retornar Response ou dict"})

    except Exception:
        q.put({"__error__": "runtime_exception", "trace": traceback.format_exc()})


def main():
    # carregar input.json
    try:
        with open("input.json") as f:
            input_data = json.load(f)
    except Exception as e:
        print(json.dumps({"__error__": "invalid_input", "detail": str(e)}))
        sys.exit(1)

    # carregar main.py
    try:
        spec = importlib.util.spec_from_file_location("user_main", "main.py")
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)
    except Exception:
        print(json.dumps({"__error__": "import_failed", "trace": traceback.format_exc()}))
        sys.exit(1)

    # executar em subprocesso com timeout
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=run_user, args=(q, input_data, user_module))
    p.start()
    p.join(TIMEOUT)

    if p.is_alive():
        p.terminate()
        print(json.dumps({"__error__": "timeout", "detail": f"exceeded {TIMEOUT}s"}))
        sys.exit(1)

    try:
        out = q.get_nowait()
        if "__result__" in out:
            try:
                print(json.dumps(out["__result__"]))
            except Exception:
                print(json.dumps({"__error__": "serialization_error"}))
                sys.exit(1)
            sys.exit(0)
        else:
            print(json.dumps(out))
            sys.exit(1)
    except queue.Empty:
        print(json.dumps({"__error__": "no_output", "detail": "user code did not return"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
