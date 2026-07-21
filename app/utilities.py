from .database_models import Post, User


def get_user_by_id(session, user_id):
    return session.query(User).filter(User.id == user_id).first()


def get_user_by_username(session, username):
    return session.query(User).filter(User.username == username).first()


def get_user_by_email(session, email):
    return session.query(User).filter(User.email == email).first()


def new_user(session, username, email, password):
    from .security import get_password_hash

    hashed_password = get_password_hash(password)
    new_user_obj = User(username=username, email=email, password=hashed_password)
    session.add(new_user_obj)
    session.commit()
    session.refresh(new_user_obj)
    return new_user_obj

def get_id_by_username(session, username):
    user = session.query(User).filter(User.username == username).first()
    if user:
        return user.id
    return None
    
def new_post(session, title, content, user_id):
    new_post_obj = Post(title=title, content=content, user_id=user_id)
    session.add(new_post_obj)
    session.commit()
    session.refresh(new_post_obj)
    return new_post_obj


def delete_post(session, post_id):
    post = session.query(Post).filter(Post.id == post_id).first()
    if post is not None:
        session.delete(post)
        session.commit()
    return post