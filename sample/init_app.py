from pathlib import Path
from tempfile import TemporaryDirectory

from sample.app import MultiPageApp
from sample.const import PageId
from sample.pages.base import BasePage
from sample.pages.member.cart import CartPage
from sample.pages.member.order_detail import OrderDetailPage
from sample.pages.member.order_list import OrderListPage
from sample.pages.public.item_detail import ItemDetailPage
from sample.pages.public.item_list import ItemListPage
from sample.pages.public.login import LoginPage
from sample.services.auth import MockAuthAPIClientService
from sample.services.cart import MockCartAPIClientService
from sample.services.item import MockItemAPIClientService
from sample.services.mock import MockDB, MockSessionDB
from sample.services.order import MockOrderAPIClientService
from sample.services.user import MockUserAPIClientService
from sample.sesseion import StreamlitSessionManager


def init_session() -> StreamlitSessionManager:
    mockdir = Path(TemporaryDirectory().name)
    mockdir.mkdir(exist_ok=True)
    mockdb = MockDB(mockdir.joinpath("mock.db"))
    session_db = MockSessionDB(mockdir.joinpath("session.json"))
    ssm = StreamlitSessionManager(
        auth_api_client=MockAuthAPIClientService(mockdb, session_db),
        user_api_client=MockUserAPIClientService(mockdb, session_db),
        item_api_client=MockItemAPIClientService(mockdb),
        order_api_client=MockOrderAPIClientService(mockdb, session_db),
        cart_api_client=MockCartAPIClientService(session_db),
    )
    return ssm


def init_pages(ssm: StreamlitSessionManager) -> list[BasePage]:
    pages = [
        LoginPage(page_id=PageId.PUBLIC_LOGIN, title="ログイン", ssm=ssm),
        ItemListPage(page_id=PageId.PUBLIC_ITEM_LIST, title="商品一覧", ssm=ssm),
        ItemDetailPage(page_id=PageId.PUBLIC_ITEM_DETAIL, title="商品詳細", ssm=ssm),
        CartPage(page_id=PageId.MEMBER_CART, title="カート", ssm=ssm),
        OrderListPage(page_id=PageId.MEMBER_ORDER_LIST, title="注文一覧", ssm=ssm),
        OrderDetailPage(page_id=PageId.MEMBER_ORDER_DETAIL, title="注文詳細", ssm=ssm),
    ]
    return pages


def init_app(ssm: StreamlitSessionManager, pages: list[BasePage]) -> MultiPageApp:
    app = MultiPageApp(ssm, pages)
    return app
