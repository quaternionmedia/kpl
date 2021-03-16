from kpl.api import app

def main():
    from uvicorn import run
    run(app, host='0.0.0.0', port=8888)

if __name__ == '__main__':
    main()