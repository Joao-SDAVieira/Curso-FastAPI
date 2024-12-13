from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(username="João", email="joao@ao.com", password="minha_senha11")

    session.add(user)  # adicionando usuário ao banco,sem de fato adicionar

    session.commit()  # fazendo de fato a modificação no banco

    # session.refresh(user)  # aqui sincroniza o objeto python
    # # com o do banco com isso o objeto passa a ter
    # # por exemplo o id pois o banco adicionou
    result = session.scalar(select(User).where(User.email == "joao@ao.com"))
    assert result.username == "João"
