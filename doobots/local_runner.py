#!/usr/bin/env python3
import sys, json, importlib.util, traceback
import multiprocessing, queue
from pathlib import Path
from doobots import Request, Response

TIMEOUT = 900  # segundos

def run_user(q, data):
    try:
        possible_paths = [Path("main.py"), Path("app") / "main.py"]
        file_path = None
        for path in possible_paths:
            if path.exists():
                file_path = path
                break

        if not file_path:
            raise FileNotFoundError("main.py não encontrado em ./ ou ./app/")

        spec = importlib.util.spec_from_file_location("user_main", str(file_path))
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)

        if not hasattr(user_module, "main"):
            q.put({"__error__": "no_main", "detail": "O módulo importado não possui uma função 'main'."})
            return

        request_data = data.get("data", {})
        input_files = data.get("files", [])

        result = user_module.main(Request(request_data, input_files))

        if isinstance(result, Response):
            q.put({"__result__": result.to_dict()})
        elif isinstance(result, dict):
            q.put({"__result__": result})
        else:
            q.put({"__error__": "invalid_return", "detail": "main deve retornar Response ou dict"})
    except Exception:
        q.put({"__error__": "runtime_exception", "trace": traceback.format_exc()})


def main():
    try:
        with open("input.json") as f:
            input_data = json.load(f)
    except Exception as e:
        print(json.dumps({"__error__": "invalid_input", "detail": "Não foi possível encontrar o arquivo de entrada 'input.json'."}))
        return 1

    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=run_user, args=(q, input_data))
    p.start()
    p.join(TIMEOUT)

    if p.is_alive():
        p.terminate()
        print(json.dumps({"__error__": "timeout", "detail": f"Excedeu o tempo limite de {TIMEOUT}s"}))
        return 1

    try:
        out = q.get_nowait()
        if "__result__" in out:
            try:
                print(json.dumps(out["__result__"]))
            except Exception:
                print(json.dumps({"__error__": "Erro ao serializar a resposta para JSON"}))
                return 1
            return 0
        else:
            print(json.dumps(out))
            return 1
    except queue.Empty:
        print(json.dumps({"__error__": "no_output", "detail": "O código do usuário não retornou nada."}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
