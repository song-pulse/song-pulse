#  TODO: give a valid songid from our db


def action_state_to_song(self):
    """
    TODO: put this in another file in util/action_song_converter.py
    this function takes an action and state(the optimal action for the given state computed and chooses a song
    randomly from one of the 3 spotify playlists)
    :return: song from spotify either the song link or directly play the song here
    """
    if self.action == 0 & self.state == 0:
        self.playlist_id = 0
    if self.action == 1 & self.state == 0:
        self.playlist_id = 0
    if self.action == 2 & self.state == 0:
        self.playlist_id = 1
    if self.action == 0 & self.state == 1:
        self.playlist_id = 0
    if self.action == 1 & self.state == 1:
        self.playlist_id = 1
    if self.action == 2 & self.state == 1:
        self.playlist_id = 2
    if self.action == 0 & self.state == 2:
        self.playlist_id = 0
    if self.action == 1 & self.state == 2:
        self.playlist_id = 2
    if self.action == 2 & self.state == 2:
        self.playlist_id = 2
    print('playlist_id', self.playlist_id)
    return self.playlist_id