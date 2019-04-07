 import time
from random import randint
from datalayer import InstalikeDataLayer


class InstaFollow:
    def __init__(self, operation, repository: InstalikeDataLayer, content_manager, configuration):
        self.operation = operation
        self.repository = repository
        self.content_manager = content_manager
        self.configuration = configuration

        # configuration
        self.max_follows_per_hour = self.configuration.instafollow_max_follows_per_hour
        self.max_unfollows_per_hour = self.configuration.instafollow_max_unfollows_per_hour
        self.unfollow_users = self.configuration.instafollow_unfollow_users  # unfollow ppl?
        self.unfollow_after_days = self.configuration.instafollow_unfollow_after_days  # unfollow people after # days
        # users
        self.users = []
        self.to_unfollow = []

        # instance stats
        self.follows = 0
        self.unfollows = 0
        self.failed_follows = 0
        self.failed_unfollows = 0

        self.hourly_follows = 0
        self.hourly_unfollows = 0

        # timing
        self.next_follow_time = 0
        self.next_unfollow_time = 0

        self.follow_time_delta = 60 * 60 // (1 if self.max_follows_per_hour == 0 else self.max_follows_per_hour)
        self.unfllow_time_delta = 60 * 60 // (1 if self.max_unfollows_per_hour == 0 else self.max_unfollows_per_hour)

        self.next_unfollow_queue_update = 0  # when to update users that bot will unfollow

        self.t0 = time.time()
        self.t1 = 0

    def follow(self):
        if (time.time() < self.next_follow_time):
            return

        user = self.content_manager.get_next_user()
        if (user != None):
            response = self.operation.follow(user.id)
            self.repository.persist_follow(user)

        if (response.status_code != 200):
            self.failed_follow()
        else:
            self.followed_successfully(user)

        self.update_follow_timer()

    def unfollow(self):
        if not self.unfollow_users or (time.time() < self.next_unfollow_time):
            return

        if len(self.to_unfollow) == 0:
            self.to_unfollow = self.repository.get_users_to_unfollow(self.configuration.instafollow_unfollow_after_days)

        if len(self.to_unfollow) > 0:
            user_id = self.to_unfollow.pop()
            response = self.operation.unfollow(user_id)
            self.repository.persist_unfollow(user_id, response.status_code)

            if (response.status_code != 200):
                self.failed_unfollow()
            else:
                self.unfollowed()
            self.update_unfollow_timer()


    def act(self):
        self.follow()
        self.unfollow()

    def update_follow_timer(self):
        self.next_follow_time = time.time() + randint(self.follow_time_delta - (self.follow_time_delta // 2),
                                                      self.follow_time_delta + (self.follow_time_delta // 2))
        self.get_stats()

    def update_unfollow_timer(self):
        self.next_unfollow_time = time.time() + randint(self.unfllow_time_delta - (self.unfllow_time_delta // 2),
                                                        self.unfllow_time_delta + (self.unfllow_time_delta // 2))
        self.get_stats()

    def get_stats(self):
        self.t1 = time.time()
        per_hour_follows = ((self.follows + self.failed_follows) * 60 * 60) // (
        1 if (self.t1 - self.t0) == 0 else self.t1 - self.t0)
        per_hour_unfollows = ((self.unfollows + self.failed_unfollows) * 60 * 60) // (
        1 if (self.t1 - self.t0) == 0 else self.t1 - self.t0)
        self.log('#######################################')
        self.log('---------------FOLLOWS-----------------')
        self.log('total time: {0:.0f}s'.format(self.t1 - self.t0))
        self.log('follows: {0}'.format(self.follows))
        self.log('failed follows: {0}'.format(self.failed_follows))
        if (self.unfollow_users):
            self.log('unfollows: {0}'.format(self.unfollows))
            self.log('failed unfollows: {0}'.format(self.failed_unfollows))
        self.log('estimated follows per hour: {0:.0f}'.format(per_hour_follows))
        if (self.unfollow_users):
            self.log('estimated unfollows per hour: {0:.0f}'.format(per_hour_unfollows))
        self.log('next follow in: {0:.0f}s'.format(self.next_follow_time - time.time()))
        if (self.unfollow_users):
            self.log('next unfollow in: {0:.0f}s'.format(
                0 if self.next_unfollow_time == 0 else self.next_unfollow_time - time.time()))
        self.log('users to follow: {0}'.format(self.content_manager.get_user_count()))
        if (self.unfollow_users):
            self.log('users to unfollow: {0}'.format(len(self.to_unfollow)))

    def log(self, text):
        print(text)

    def failed_unfollow(self):
        self.failed_unfollows += 1

    def unfollowed(self):
        self.unfollows += 1

    def failed_follow(self):
        self.failed_follows += 1

    def followed_successfully(self, user):
        self.follows += 1
        self.hourly_follows += 1
