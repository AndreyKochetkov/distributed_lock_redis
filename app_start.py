from time import sleep, clock
from Generator import Generator

def main():
    # TODO: сделать так, чтобы можно было определить через redis сколько приложений запущено
    generator = Generator("localhost", 6379, 0, 1)
    try:
        generator.generate_messages()
    except Exception as e:
        print("Error: " + str(e))




if __name__ == "__main__":
    main()
