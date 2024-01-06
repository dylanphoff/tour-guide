from dotenv import load_dotenv

from tour_guide import TourGuide


def main():
    load_dotenv()
    tour_guide = TourGuide()
    tour_guide.run()


if __name__ == "__main__":
    main()
