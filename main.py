import recognition_voice


def main():
    voice = recognition_voice.Recognition(
        path="./voice_models/vosk-model-ru-0.10"
    )
    listen_voice = voice.listen()

    print('Jarvis is ready...')
    for text in listen_voice:
        text_words = text.split(" ")
        if text_words[0] == "джарвис":
            text = " ".join(text_words[1:])
            if text in ["пока", "досвидание", "удачи"]:
                print("Досвидание")
                quit()
            print(text)


if __name__ == "__main__":
    main()
