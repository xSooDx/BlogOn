class Post:
    def __init__(self, postid, userid, title, content, description=None, tags=None, ptype=0, img=None, categories=None):
        self.postid = postid
        self.userid = userid
        self.title = title
        self.content = content
        self.description = description
        self.tags = tags
        self.img = img
        self.type = ptype
        self.categories = categories


class Page:
    def __init__(self, pageid, title, content, description=None):
        self.pageid = pageid
        self.title = title
        self.content = content
        self.description = description


class User:
    def __init__(self, userid, username, email, rank=None, token=None):
        self.userid = userid
        self.username = username
        self.email = email
        self.rank = rank
        self.token = token


class Comment:
    def __init__(self, commentid, postid, email, name, comment):
        self.commentid = commentid
        self.postid = postid
        self.email = email
        self.name = name
        self.comment = comment
