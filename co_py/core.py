# AUTOGENERATED! DO NOT EDIT! File to edit: codeforces_python_client.ipynb (unless otherwise specified).


from __future__ import print_function, division


__all__ = ['Card', 'Base', 'Contest', 'User', 'Problem', 'UserRating', 'BlogEntry', 'Comment', 'Party',
           'ProblemStatistics', 'ProblemResult', 'RecentAction', 'Hack', 'Submission', 'RanklistRow', 'Standings',
           'CFApi']

# Cell
#nbdev_comment from __future__ import print_function, division

import random

class Card:
    """Represent a standard playing card.

    Attributes:
        suit: integer 0-3
        rank: integer 1-13
    """

    suit_names = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    rank_names = [None, 'Ace', '2', '3', '4', '5', '6', '7']

    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        """Returns a human-readable string representation"""
        return '%s of %s' % (Card.rank_names[self.rank], Card.suit_names[self.suit])

    def __repr__(self):
        return self.__str__()

# Cell
import datetime
import time
import random
import string

import requests
import inflection

# Cell
class Base:
    _fields = None
    def __init__(self, content: dict) -> None:
        self.init(content)

    def init(self, content: dict) -> None:
        if not self._fields:
            raise ValueError('_fields is not set for the class')
        for field, val_type in self._fields.items():
            val = content.get(field)
            if val is None:
                setattr(self, inflection.underscore(field), val)
            else:
                setattr(self, inflection.underscore(field), val_type(val))

    def __repr__(self):
        return str(self.__dict__)

# Cell
class Contest(Base):
    _fields = {
        'id': int,
        'name': str,
        'type': str,
        'phase': str,
        'frozen': bool,
        'durationSeconds': int,
        'startTimeSeconds': int,
        'relativeTimeSeconds': int,
        'preparedBy': int,
        'websiteUrl': str,
        'description': str,
        'difficulty': int,
        'kind': str,
        'icpcRegion': str,
        'country': str,
        'city': str,
        'season': str,
    }

    def __init__(self, contest):
        super().__init__(contest)
        self.duration_hours = self.duration_seconds / (60*60)
        if self.start_time_seconds:
            self.start_time = datetime.datetime.fromtimestamp(self.start_time_seconds)
            self.end_time = self.start_time + datetime.timedelta(seconds=self.duration_seconds)


class User(Base):
    _fields = {
        'handle': str,
        'email': str,
        'vkId': str,
        'openId': str,
        'firstName': str,
        'lastName': str,
        'country': str,
        'city': str,
        'organization': str,
        'contribution': int,
        'rank': str,
        'rating': int,
        'maxRank': str,
        'maxRating': int,
        'lastOnlineTimeSeconds': int,
        'registrationTimeSeconds': int,
        'friendOfCount': int,
        'avatar': str,
        'titlePhoto': str
    }


class Problem(Base):
    _fields = {
        'contestId': int,
        'problemsetName': str,
        'index': str,
        'name': str,
        'type': str,
        'points': float,
        'rating': int,
        'tags': list
    }


class UserRating(Base):
    _fields = {
        'contestId': int,
        'contestName': str,
        'handle': str,
        'rank': int,
        'ratingUpdateTimeSeconds': int,
        'oldRating': int,
        'newRating': int
    }


class BlogEntry(Base):
    _fields = {
        'id': int,
        'originalLocale': str,
        'creationTimeSeconds': int,
        'authorHandle': str,
        'title': str,
        'content': str,
        'locale': str,
        'modificationTimeSeconds': int,
        'allowViewHistory': bool,
        'tags': list,
        'rating': int
    }


class Comment(Base):
    _fields = {
        'id': int,
        'creationTimeSeconds': int,
        'commentatorHandle': str,
        'locale': str,
        'text': str,
        'parentCommentId': int,
        'rating': int
    }



class Party(Base):
    _fields = {
        'contestId': int,
        'members': list,
        'participantType': str,
        'teamId': int,
        'teamName': str,
        'ghost': bool,
        'room': int,
        'startTimeSeconds': int
    }


class ProblemStatistics(Base):
    _fields = {
        'contestId': int,
        'index': str,
        'solvedCount': int
    }


class ProblemResult(Base):
    _fields = {
        'points': float,
        'penalty': int,
        'rejectedAttemptCount': int,
        'type': str,
        'bestSubmissionTimeSeconds': int
    }


class RecentAction(Base):
    _fields = {
        'timeSeconds': int,
        'blogEntry': BlogEntry,
        'comment': Comment
    }


class Hack(Base):
    _fields = {
        'id': int,
        'creationTiemSeconds': int,
        'hacker': Party,
        'defender': Party,
        'verdict': str,
        'problem': Problem,
        'test': str,
        'judgeProtocol': object
    }


class Submission(Base):
    _fields = {
        'id': int,
        'contestId': int,
        'creationTimeSeconds': int,
        'relativeTimeSeconds': int,
        'problem': Problem,
        'author': Party,
        'programmingLanguage': str,
        'verdict': str,
        'testset': str,
        'passedTestCount': int,
        'timeConsumedMillis': int,
        'memoryConsumedBytes': int,
        'points': float
    }


class RanklistRow(Base):
    _fields = {
        'party': Party,
        'rank': int,
        'points': float,
        'penalty': int,
        'successfulHackCount': int,
        'unsuccessfulHackCount': int,
        'problemResults': list,
        'lastSubmissionTimeSeconds': int
    }


class Standings(Base):
    _fields = {
        'contest': Contest,
        'problems': list,
        'rows': list,
    }

# Cell
class CFApi:
    _url_pack = {
        'blog.comments': 'https://codeforces.com/api/blogEntry.comments',
        'blog.view': 'https://codeforces.com/api/blogEntry.view',
        'contest.list': 'https://codeforces.com/api/contest.list',
        'contest.standings': 'https://codeforces.com/api/contest.standings',
        'problemset.problems': 'https://codeforces.com/api/problemset.problems',
        'user.info': 'https://codeforces.com/api/user.info',
        'user.rating': 'https://codeforces.com/api/user.rating',
        'user.status': 'https://codeforces.com/api/user.status',
    }

    _BASE_API = 'https://codeforces.com/api/'

    def __init__(self, api_key=None, secret=None, lang='eu'):
        self.api_key = api_key
        self.secret = secret
        self.lang = lang
        self.anonymous = True
        # check for supply of both
        if self.api_key and self.secret:
            self.anonymous = False


    def _generate_secret_params(self, method_name: str, params) -> dict:
        cur_time = int(time.time())
        rand_char = random.choices(string.printable, k=6)
        rand_char = "".join(rand_char)

        sorted_params = {key: val for key, val in sorted(params.items())}  # only for Python3.6 and above
        params_encoded = requests.urllib3.request.urlencode(sorted_params)

        api_sig = f'{rand_char}/{method_name}?{params_encoded}#{self.secret}'
        api_sig = hashlib.sha512(api_sig)
        secret_params = {
            'apiKey': self.api_key,
            'time': str(cur_time),
            'apiSig': api_sig
        }
        return secret_params


    def _get_data(self, method_name: str, params: dict = None):
        url = self._BASE_API + method_name
        cur_time = datetime.datetime.now().timestamp()
        if params is None:
            params = {}

        if not self.anonymous:
            secret_params = self._generate_secret_params(method_name, params)
            params.update(secret_params)

        res = requests.get(url, params=params)
        if res.status_code != 200:
            pass # raise Error
        res = res.json()
        if res['status'] != 'OK':
            raise Exception(res)
        return res['result']


    def get_contests(self, gym=False):
        method_name = 'contest.list'
        params = {'gym': gym}
        contests = self._get_data(method_name, params)
        contests = [Contest(contest) for contest in contests]
        return contests


    def get_problems(self, tags=None):
        method_name = 'problemset.problems'
        if isinstance(tags, str):
            tags = [tags]
        if tags:
            tags = ";".join(tags)
        params = {'tags': tags}
        res = self._get_data(method_name, params)
        problems = [Problem(problem) for problem in res['problems']]
        return problems


    def get_user_info(self, handles):
        method_name = 'user.info'
        if isinstance(handles, str):
            handles = [handles]
        handles = ";".join(handles)
        params = {'handles': handles}
        users = self._get_data(method_name, params)
        users = [User(user) for user in users]
        return users


    def get_user_ratings(self, handle):
        method_name = 'user.rating'
        params = {'handle': handle}
        user_ratings = self._get_data(method_name, params)
        user_ratings = [UserRating(rating) for rating in user_ratings]
        return user_ratings


    def get_user_submissions(self, handle: str):
        # from and count
        method_name = 'user.status'
        params = {'handle': handle}
        submissions = self._get_data(method_name, params)
        submissions = [Submission(submission) for submission in submissions]
        return submissions


    def get_blog_comments(self, blog_id: int) -> Comment:
        method_name = 'blogEntry.comments'
        params = {'blogEntryId': blog_id}
        comments = self._get_data(method_name, params)
        comments = [Comment(comment) for comment in comments]
        return comments


    def get_blog_entry(self, blog_id: int) -> BlogEntry:
        method_name = 'blogEntry.comments'
        params = {'blogEntryId': blog_id}
        blog = self._get_data(method_name, params)
        blog = BlogEntry(blog)
        return blog

    def get_contest_standings(self, contest_id: int):
        method_name = 'contest.standings'
        params = {'contestId': contest_id}
        standings = self._get_data(method_name, params)
        standings = Standings(standings)
        return standings