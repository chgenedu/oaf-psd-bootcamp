from data_service import DataServiceFactory
import data_handler as dh


def main():
    print("Begin program.")

    # setup the data_service
    data_source = "config.json"
    data_service = DataServiceFactory(data_source, mode="API").create()

    # handle the data from data_service
    dh.data_handler(data_service)
    
    print("Program finished.")


if __name__ == "__main__":
    main()
