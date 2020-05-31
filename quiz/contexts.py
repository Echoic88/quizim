from .models import PlayedQuiz, PlayerAnswer, User


def percentage_correct_answers(player):
    """
    Calculate the percentage of correct answers for a given player
    """
    try:
        player_answers = PlayerAnswer.objects.filter(player=player)
        count_player_answers = player_answers.count()
        correct_answers = player_answers.filter(correct=True).count()
        percentage_correct = int(float(format((
            correct_answers/count_player_answers), ".2f"))*100)

        return percentage_correct

    except:
        return 0


def quizes_data(request):
    """
    Return context quiz data for:
    Number of quizes played and percentage questions correct for logged in user
    Leaderboard data (top 5 players)
    """
    if request.user.is_authenticated:
        number_quizes_played = PlayedQuiz.objects.filter(
            player=request.user).count()
        user_percentage_correct = percentage_correct_answers(request.user)

        score_list = []

        players = User.objects.exclude(username="admin")
        for player in players:
            score = percentage_correct_answers(player)
            score_list.append({
                "player": player,
                "score": score
            })

        leaderboard = sorted(
            score_list, key=lambda k: k["score"], reverse=True)

        return {
            "number_quizes_played": number_quizes_played,
            "user_percentage_correct": user_percentage_correct,
            "leaderboard": leaderboard
        }

    else:
        return {}
