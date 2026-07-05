from core.version import APP_NAME, VERSION, BUILD, STATUS


def show_banner():
    print("=" * 60)
    print(APP_NAME)
    print(f"Version : {VERSION}")
    print(f"Build   : {BUILD}")
    print(f"Status  : {STATUS}")
    print("=" * 60)