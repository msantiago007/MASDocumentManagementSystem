import pyodbc

def main():
    drivers = pyodbc.drivers()
    print("Available ODBC drivers:")
    for driver in drivers:
        print(f"- {driver}")

if __name__ == "__main__":
    main()