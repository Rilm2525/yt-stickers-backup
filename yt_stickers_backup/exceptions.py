class ChannelNotFoundError(Exception):
    def __init__(self, channel_handle):
        super().__init__(f"Channel ({channel_handle}) is not found.")

class SponsorIsNotActivatedError(Exception):
    def __init__(self, channel_handle):
        super().__init__(f"The channel ({channel_handle}) has not enabled the sponsor feature.")

class SponsorTierLoadError(Exception):
    def __init__(self):
        super().__init__(f"Failed to load sponsor tiers.")