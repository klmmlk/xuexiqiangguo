import time

from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.extensions.android.nativekey import AndroidKey
from tools import get_anser, get_string_diff
from appium.webdriver.webelement import WebElement

desired_caps = {
    'platformName': 'Android',  # 被测手机是安卓
    'platformVersion': '8',  # 手机安卓版本
    'deviceName': 'Mi_10',  # 设备名，安卓手机可以随意填写
    'appPackage': 'cn.xuexi.android',  # 启动APP Package名称
    'appActivity': 'com.alibaba.android.rimet.biz.SplashActivity',  # 启动Activity名称
    'noReset': True,  # 不要重置App
    'newCommandTimeout': 10000,
    # 'automationName': 'UiAutomator2',
    # 'chromeOptions': {'w3c': False}
}

# 连接Appium Server，初始化自动化环境
# driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver = webdriver.Remote('http://docker.jokerin.icu:4723/wd/hub', desired_caps)

# 设置缺省等待时间
driver.implicitly_wait(5)


# # 进入我的
# driver.find_element(By.ID, 'comm_head_xuexi_mine').click()
# # 点击学习积分
# driver.tap([(224, 815)], 100)
# driver.swipe(start_x=500, start_y=1800, end_x=500, end_y=1000, duration=800)


def swipe(lengh, duration=800):
    driver.swipe(start_x=500, start_y=1500, end_x=500, end_y=1500 - lengh, duration=duration)


# 学文章
def study_article():
    def once_read(article_node: WebElement):
        height = article_node.rect['height']
        article_node.click()
        for i in range(5):
            time.sleep(10)
            swipe(600)
        driver.press_keycode(AndroidKey.BACK)
        return height

    # 点击进入要闻
    driver.find_element(By.XPATH, '//android.view.ViewGroup/android.widget.LinearLayout[2]').click()
    time.sleep(1)
    for i in range(10):
        each_node = driver.find_element(By.XPATH,
                                        '//android.widget.FrameLayout/android.widget.ListView/android.widget'
                                        '.FrameLayout')
        node_height = once_read(each_node)
        time.sleep(0.3)
        swipe(node_height if node_height > 30 else 50, 100)
        time.sleep(1)


# 看视频
def watch_video():
    def once_watch():
        video_node = driver.find_element(By.XPATH, '//android.widget.ListView/android.widget.FrameLayout')
        height = video_node.rect['height']
        video_time = None
        try:
            video_time = video_node.find_element(By.XPATH,
                                                 '//android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.TextView').text
        except:
            if not video_time:
                try:
                    video_time = video_node.find_element(By.ID,
                                                         'st_feeds_card_play_time').text
                except:
                    swipe(height if height > 30 else 50, 100)
                    return

        video_time = video_time.split(':')
        times = int(video_time[0]) * 60 + int(video_time[1])
        # print(f'视频时长{times}秒')
        video_node.click()
        time.sleep(times + 3)
        driver.press_keycode(AndroidKey.BACK)
        time.sleep(1)
        swipe(height if height > 30 else 50, 100)
        return [True, times]
        pass

    # 进入视频页面
    driver.find_element(By.XPATH, '//android.widget.FrameLayout[@content-desc="电视台"]').click()
    swipe(96)
    video_nums = 0
    video_lens = 0
    while True:
        result = once_watch()
        if isinstance(result, list):
            video_nums += 1
            video_lens += result[1]
            print(f'已观看{video_nums}个视频')
        if video_nums == 6 and video_lens >= 600:
            print(f'观看完毕')
            break
        time.sleep(1)


# 答题操作函数
def dati_test(fn):
    # 进入我的
    driver.find_element(By.ID, 'comm_head_xuexi_mine').click()
    time.sleep(0.5)
    # 点击我要答题
    driver.tap([(546, 600)])
    time.sleep(1)
    # 检测是否是弹窗
    try:
        close_btn = driver.find_element(By.XPATH, '//android.view.View[@text="去看看"]/../../android.view.View')
    except:
        pass
    else:
        close_btn.click()
        time.sleep(0.5)
    # 外部函数，各种答题
    fn()
    driver.press_keycode(AndroidKey.BACK)
    time.sleep(0.5)
    driver.press_keycode(AndroidKey.BACK)


@dati_test
def daily_test():
    # 进入每日答题
    driver.find_element(By.XPATH,
                        '//android.webkit.WebView/android.view.View/android.view.View/android.view.View[3]/android.view.View[3]').click()
    time.sleep(0.5)

    def test_contr():
        qus_type = driver.find_element(By.XPATH,
                                       '//android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View/android.view.View/android.view.View[1]/android.view.View[1]').text
        qus_text = driver.find_element(By.XPATH,
                                       '//android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View/android.view.View/android.view.View[2]').text

        # 获取提示文本并获取答案
        # 显示提示
        driver.find_element(By.XPATH,
                            '//android.view.View[@text="查看提示"]/..').click()
        time.sleep(0.8)
        tips_text = driver.find_element(By.XPATH,
                                        '//android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View[3]/android.view.View[2]/android.view.View').text
        time.sleep(0.8)
        # 关闭提示
        driver.find_element(By.XPATH,
                            '//android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View[3]/android.view.View[1]/android.view.View[2]').click()
        # 获取答案
        if tips_text == '请观看视频':
            anser_list = get_anser(qus_text)
        else:
            anser_list = get_string_diff(qus_text, tips_text)

        if qus_type == '单选题' or qus_type == '多选题':
            # 获取题目答案选项
            sec_list_node = driver.find_elements(By.XPATH,
                                                 '//android.widget.ListView/android.view.View/android.view.View/android.view.View[2]')
            sec_list = []
            for each in sec_list_node:
                sec_list.append(each.text)
            right_anser_list = list(set(sec_list) & set(anser_list))
            for i in right_anser_list:
                driver.find_element(By.XPATH, f'//android.view.View[@text="{i}"]').click()
                time.sleep(0.2)
            if not right_anser_list:
                driver.find_element(By.XPATH,
                                    '//android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View/android.view.View/android.widget.ListView/android.view.View[1]/android.view.View').click()

        elif qus_type == '填充题':
            if anser_list:
                driver.find_element(By.XPATH, '//android.widget.EditText').send_keys(anser_list[0])
            else:
                driver.find_element(By.XPATH, '//android.widget.EditText').send_keys('强国')
            time.sleep(0.2)

        driver.find_element(By.XPATH, '//android.view.View[@text="确定"]').click()
        try:
            driver.find_element(By.XPATH, '//android.view.View[@text="下一题"]').click()
        except:
            pass

    for i in range(5):
        test_contr()
        if i == 4:
            driver.find_element(By.XPATH, '//android.view.View[@text="完成"]').click()


pass
# study_article()
# watch_video()
daily_test()
pass

driver.quit()
