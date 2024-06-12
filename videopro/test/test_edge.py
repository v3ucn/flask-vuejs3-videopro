from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(channel="msedge", headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8080/reg")
    page.get_by_text("视频平台/注册/用户名密 码手机号提 交").click()
    page.get_by_placeholder("请输入用户名").click()
    page.get_by_placeholder("请输入用户名").fill("999")
    page.get_by_placeholder("请输入密码").click()
    page.get_by_placeholder("请输入密码").fill("999")
    page.get_by_placeholder("请输入手机号").click()
    page.get_by_placeholder("请输入手机号").fill("999")
    page.get_by_role("button", name="提 交").click()
    page.locator("div").filter(has_text=re.compile(r"^提 交$")).nth(3).click()
    page.get_by_placeholder("请输入用户名").click()
    page.get_by_placeholder("请输入用户名").fill("7897979789")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
