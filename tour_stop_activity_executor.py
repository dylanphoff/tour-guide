from common.tour_stop_activity import (
    TourStopActivity,
    TourStopActivityType,
    TriviaActivity,
)


class TourStopActivityExecutor:
    def execute_activity(self, activity: TourStopActivity) -> None:
        if activity.get_type() == TourStopActivityType.TRIVIA:
            return self._execute_trivia_activity(activity)
        raise ValueError(
            f"No tour stop activity matching {activity.get_type()}"
        )

    def _execute_trivia_activity(self, activity: TriviaActivity) -> None:
        bulleted_answer_options = self._get_bulleted_answer_options(activity)
        bulleted_answer_options_str = "\n".join(bulleted_answer_options)
        print(
            f"""
            Trivia Question\n
            {activity.question}\n
            {bulleted_answer_options_str}\n
            """
        )
        answer = input("Answer: ")
        if ord(answer) == ord("a") + activity.correct_answer_index:
            print("Correct!\n")
        else:
            correct_answer = bulleted_answer_options[
                activity.correct_answer_index
            ]
            print(f"The correct answer is {correct_answer}\n")

    def _get_bulleted_answer_options(self, activity: TriviaActivity) -> str:
        bulleted_answer_options = []
        for i, option in enumerate(activity.answer_options):
            bulleted_answer_options.append(f'{chr(ord("a") + i)} {option}')
        return bulleted_answer_options
