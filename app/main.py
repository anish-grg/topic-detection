def model():
    # import and initialize BERT model
    from models.bert import bert_foo
    bert_foo()
    
def export_tweet():
    from data.data_preparation import export_tweet_dataframe
    export_tweet_dataframe()

def main():
    print('This is main function')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', type=str, default=None)
    args = parser.parse_args()
    task = args.task
    if task == 'model':
        model()
    elif task == 'export':
        export_tweet()
    else:
        main()
