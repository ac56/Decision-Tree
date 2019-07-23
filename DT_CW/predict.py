import setup


def predict_label ( tree, data ):
    
    if( tree['leaf'] == True):
        #print('alow')
        return tree['value']
    else:
        if ( data[tree['attr']] < tree['value'] ):
            return predict_label ( tree['left'], data)
        else:
            return predict_label ( tree['right'], data)