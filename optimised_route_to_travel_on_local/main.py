import camelot
def main():
    

    # Extract tables from PDF
    tables = camelot.read_pdf('C:/Users/kapil/Downloads/central_line_.pdf', #flavor='stream'
                              )

    # Convert to DataFrame
    df = tables[0].df  # First table
    print(df)
    print("Hello from optimised-route-to-travel-on-local!")


if __name__ == "__main__":
    main()