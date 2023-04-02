from NFetcher import NFetch

def main():
    n_api = NFetch()
    
    try:
        top_n = n_api.fetch_n_top(100)
        assert(len(top_n) <= 100)
        all_top = n_api.fetch_top()
        print('Total leading articles: ', len(all_top))
        for news in all_top:
            print(f"author: {news['author']}, title: {news['title']}")
        for news in n_api.search_by_title('AI'):
            print(f"author: {news['author']}, title: {news['title']}")
        for news in n_api.search_for_article('ChatGPT'):
            print(f"author: {news['author']}, title: {news['title']}")
        for news in n_api.search_by_author('bbc'):
            print(f"author: {news['author']}, title: {news['title']}")

        # n_api.clear_cache()
    except Exception as err:
        n_api.graceful_exit()
        raise err

    n_api.graceful_exit()

if __name__ == '__main__':
    main()