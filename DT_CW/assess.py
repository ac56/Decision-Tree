import setup

def set_score ( prediction_list, answers ):
    print('\n' + 'entered set_score function')
    print('prediction list:')
    print(prediction_list)
    print('answers:')
    print(answers)
    correct_predictions = 0
    if ( len(prediction_list) != len(answers) ):
        return "Cannot assess prediction list as it has a different length to the answers list"
    else:
        for i in range(len(prediction_list)):
            if ( prediction_list[i] == answers[i]):
                correct_predictions += 1
    return (correct_predictions/len(prediction_list)) * 100

