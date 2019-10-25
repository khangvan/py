def testrun():
  print("ok")
def testrun2():
  return "hii"
  
def postgres_passwd(password, username, uppercase=False):
    """
    Reference(s):
        http://pentestmonkey.net/blog/cracking-postgres-hashes/
    >>> postgres_passwd(password='testpass', username='testuser', uppercase=False)
    'md599e5ea7a6f7c3269995cba3927fd0093'
    """

    username = getBytes(username)
    password = getBytes(password)

    retVal = "md5%s" % md5(password + username).hexdigest()

    return retVal.upper() if uppercase else retVal.lower()
