import matplotlib.pyplot as plt


"""
Функция для отображения графика функции потерь и метрики 
на основе истории логов log_history обучения модели библиотеки transformers (hugginface)
"""
def log_history_to_plot(log_history):
    train_losses = []
    eval_losses = []
    n_epochs = 0

    f1_values_val = []
    for log in log_history:
        if "loss" in log.keys():
            train_losses.append(log["loss"])
            n_epochs = int(log["epoch"])
        if "eval_loss" in log.keys():
            eval_losses.append(log["eval_loss"])
            f1_values_val.append(log["eval_f1"])
    
    
    fig, ax = plt.subplots(1, 2, figsize=(16, 4))

    ax[0].plot(train_losses, label="Train")
    ax[0].plot(eval_losses, label="Validation")

    # ax[0].set_xticks([i + 1 for i in range(n_epochs)])
    ax[0].set_xlabel("epoch")
    ax[0].set_title("Losses")

    ax[1].plot(f1_values_val, label="F1 validation")

    # ax[1].set_xticks([i + 1 for i in range(n_epochs)])
    ax[1].set_xlabel("epoch")
    ax[1].set_title("F1 metric")

    ax[0].legend(loc="upper right")
    ax[1].legend(loc="lower right")
    plt.show()