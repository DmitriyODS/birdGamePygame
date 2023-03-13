from app.app import App
from store.store import Store


def main():
    store = Store("./db")
    app = App(store)
    app.run()


if __name__ == '__main__':
    main()
