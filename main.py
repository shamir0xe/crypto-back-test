from src.delegators.app_delegator import App

def main():
    App() \
    .read_config() \
    .collect_signals() \
    .run() \
    .plot_figures() \
    .output_results()


if __name__ == '__main__':
    main()
    