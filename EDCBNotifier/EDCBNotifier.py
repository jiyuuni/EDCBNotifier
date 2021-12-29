
import colorama
import os
import sys

import config
from SendDiscord import Discord
from SendLINE import LINE
from SendTwitter import Twitter
from Utils import Utils


def main():

    # 初期化
    colorama.init(autoreset=True)
    if config.NOTIFY_LOG:  # 標準出力をファイルに変更
        sys.stdout = open(os.path.dirname(__file__) + '/' + 'EDCBNotifier.log', mode='w', encoding='utf-8')
        sys.stderr = open(os.path.dirname(__file__) + '/' + 'EDCBNotifier.log', mode='w', encoding='utf-8')

    # ヘッダー
    header = '+' * 60 + '\n'
    header += '+{:^58}+\n'.format(f'EDCBNotifier version {Utils.VERSION}')
    header += '+' * 60 + '\n'
    print('\n' + header)

    print(f'Execution Time: {Utils.getExecutionTime()}', end='\n\n')

    # 引数を受け取る
    if (len(sys.argv) > 1):

        caller = sys.argv[1]  # 呼び出し元のバッチファイルの名前
        print('Event: ' + caller, end='\n\n')

        # NOTIFY_MESSAGE にあるイベントでかつ通知がオンになっていればメッセージをセット
        if (caller in config.NOTIFY_MESSAGE and caller in config.NOTIFY_EVENT):
            message = config.NOTIFY_MESSAGE[caller]

        # NOTIFY_MESSAGE にあるイベントだが、通知がオフになっているので終了
        elif caller in config.NOTIFY_MESSAGE:
            print('Info: ' + caller + ' notification is off, so it ends.', end='\n\n')
            sys.exit(0)

        # 引数が不正なので終了
        else:
            Utils.error('Invalid argument.')

    # 引数がないので終了
    else:
        Utils.error('Argument does not exist.')

    # マクロを取得
    macros = Utils.getMacro(os.environ)
    # メッセージを置換
    for macro, macro_value in macros.items():
        # $$ で囲われた文字を置換する
        message = message.replace('$' + macro + '$', macro_value)

    print('Message: ' + message.replace('\n', '\n         '), end='\n\n')

    # 送信する画像
    # パスをそのまま利用
    if (config.NOTIFY_IMAGE is not None and os.path.isfile(config.NOTIFY_IMAGE)):
        image = config.NOTIFY_IMAGE

    # パスを取得して連結
    elif (config.NOTIFY_IMAGE is not None and os.path.isfile(os.path.dirname(__file__) + '/' + config.NOTIFY_IMAGE)):
        image = os.path.dirname(__file__) + '/' + config.NOTIFY_IMAGE

    # 画像なし
    else:
        image = None

    # LINE Notify にメッセージを送信
    if ('LINE' in config.NOTIFY_TYPE):

        line = LINE(config.LINE_ACCESS_TOKEN)

        try:
            result_line:dict = line.sendMessage(message, image_path=image)
        except Exception as error:
            print('[LINE Notify] Result: Failed')
            print('[LINE Notify] ' + colorama.Fore.RED + 'Error: ' + error.args[0], end='\n\n')
        else:
            if result_line['status'] != 200:
                # ステータスが 200 以外（失敗）
                print('[LINE Notify] Result: Failed (Code: ' + str(result_line['status']) + ')')
                print('[LINE Notify] ' + colorama.Fore.RED + 'Error: ' + result_line['message'], end='\n\n')
            else:
                # ステータスが 200（成功）
                print('[LINE Notify] Result: Success (Code: ' + str(result_line['status']) + ')')
                print('[LINE Notify] Message: ' + result_line['message'], end='\n\n')

    # Discord にメッセージを送信
    if ('Discord' in config.NOTIFY_TYPE):

        discord = Discord(config.Discord_WEBHOOK_URL)

        try:
            result_discord:dict = discord.sendMessage(message, image_path=image)
        except Exception as error:
            print('[Discord] Result: Failed')
            print('[Discord] ' + colorama.Fore.RED + 'Error: ' + error.args[0], end='\n\n')
        else:
            if result_discord['status'] != 204:
                # ステータスが 204 以外（失敗）
                print('[Discord] Result: Failed (Code: ' + str(result_discord['status']) + ')')
                print('[Discord] ' + colorama.Fore.RED + 'Error: ' + result_discord['message'], end='\n\n')
            else:
                # ステータスが 200（成功）
                print('[Discord] Result: Success (Code: ' + str(result_discord['status']) + ')', end='\n\n')

    # Twitter にツイートを送信
    if ('Tweet' in config.NOTIFY_TYPE):

        twitter = Twitter(
            config.TWITTER_CONSUMER_KEY,
            config.TWITTER_CONSUMER_SECRET,
            config.TWITTER_ACCESS_TOKEN,
            config.TWITTER_ACCESS_TOKEN_SECRET
        )

        # ツイートを送信
        try:
            result_tweet:dict = twitter.sendTweet(message, image_path=image)
        except Exception as error:
            print('[Tweet] Result: Failed')
            print('[Tweet] ' + colorama.Fore.RED + 'Error: ' + error.args[0], end='\n\n')
        else:
            print('[Tweet] Result: Success')
            print('[Tweet] Tweet: https://twitter.com/i/status/' + str(result_tweet['id']), end='\n\n')

    # Twitter にダイレクトメッセージを送信
    if ('DirectMessage' in config.NOTIFY_TYPE):

        twitter = Twitter(
            config.TWITTER_CONSUMER_KEY,
            config.TWITTER_CONSUMER_SECRET,
            config.TWITTER_ACCESS_TOKEN,
            config.TWITTER_ACCESS_TOKEN_SECRET
        )

        # ダイレクトメッセージを送信
        try:
            result_directmessage:dict = twitter.sendDirectMessage(message, image_path=image, destination=config.NOTIFY_DIRECTMESSAGE_TO)
        except Exception as error:
            print('[DirectMessage] Result: Failed')
            print('[DirectMessage] ' + colorama.Fore.RED + 'Error: ' + error.args[0], end='\n\n')
        else:
            print('[DirectMessage] Result: Success')
            print('[DirectMessage] Message: https://twitter.com/messages/' +
                  result_directmessage['event']['message_create']['target']['recipient_id'] + '-' +
                  result_directmessage['event']['message_create']['sender_id'], end='\n\n')


if __name__ == '__main__':
    main()
