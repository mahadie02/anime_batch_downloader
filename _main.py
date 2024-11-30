from controller import main_control


###___*** Only Supports downloading from https://sosukeaizen.online/ for now *** ___###

if __name__ == '__main__':
    
    # User-specified configuration
    download_folder = 'Anime'  # Folder to save all anime

    base_url = 'Link of any episode of the Anime from https://sosukeaizen.online/'
    anime_name = 'Anime Name'  # Anime name (formatted for filenames)
    season_number = 1  # Season number
    start_episode = 1  #Start of episode to download
    max_episodes = 12  # Maximum number of episodes to download
    
    main_control(base_url, download_folder,anime_name, season_number, start_episode, max_episodes)