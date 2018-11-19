import time, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from sys import platform as _platform
import getpass
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

MAX_SUBS = 1000000
MAX_CF_CONTEST_ID = 4444

SUBMISSION_URL = 'http://lightoj.com/volume_usersubmissions.php'
CODE_URL = "http://lightoj.com/volume_showcode.php?sub_id={submissionId}"

EXT = {'C++': 'cpp', 'C': 'c', 'Java': 'java', 'Python': 'py', 'Delphi': 'dpr', 'FPC': 'pas', 'C#': 'cs'}
EXT_keys = EXT.keys()

replacer = {'&quot;': '\"', '&gt;': '>', '&lt;': '<', '&amp;': '&', "&apos;": "'"}
keys = replacer.keys()

waitTime = 2


def GetPathOfChromeDriver():
    path = os.path.join(os.getcwd(), "chromedriver")
    if _platform == "linux" or _platform == "linux2":
        # linux
        path += "_linux"
    elif _platform == "darwin":
        # MAC OS X
        path += "_mac"
    elif _platform == "win32" or _platform == "win64":
        # Windows
        path += "_win"
    return path


driver = webdriver.Chrome(GetPathOfChromeDriver())


def get_ext(comp_lang):
    if comp_lang == "C++":
        return "cpp"
    elif comp_lang == "C":
        return "c"
    elif comp_lang == "JAVA":
        return "java"
    else:
        return "txt"


def parse(source_code):
    for key in keys:
        source_code = source_code.replace(key, replacer[key])

    if source_code.startswith(" ") or source_code.startswith("  "):
        if not source_code.startswith("   ") and len(source_code) > 2:
            source_code = source_code.strip()
    return source_code


def light_oj_log_in(user, passwd):
    login_site = "http://lightoj.com/login_main.php"
    login_site = SUBMISSION_URL

    for i in range(1):
        driver.get(login_site)
        username = driver.find_element_by_id("myuserid")
        password = driver.find_element_by_id("mypassword")
        driver.find_element_by_name('myrem').click()

        username.send_keys(user)
        password.send_keys(passwd)
        # time.sleep(10)

        driver.find_element_by_xpath("/html/body/div[2]/form/input").click()

        elem = driver.find_elements_by_xpath('/html/body/div[2]/h3[1]')
        if len(elem) > 0:
            print("Invalid Handle / Password")
            driver.quit()
            exit(0)


def FileNameParse(file):
    avoid = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    ret = ""
    for ch in file:
        if ch not in avoid:
            ret += ch
    return ret


def GetDownloadedFile(handle):
    path = os.path.join(handle, 'downloaded')
    if os.path.exists(path) == False:
        return []
    file = open(str(path), 'r')
    downloaded = file.readlines()
    downloaded = map(lambda s: s.strip(), downloaded)
    print("Existing: ", downloaded)
    return downloaded


def SetDownloadedFile(handle, st):
    path = os.path.join(handle, 'downloaded')
    file = open(str(path), 'a')
    file.write(st + "\n")
    file.close()


def main():
    handle = input("Enter your handle: ")
    print("Next step is password. ;) ")
    print("If you are afraid then check the code, You are smart enough to understand it")
    passwd = getpass.getpass("Enter your password: ")

    start_time = time.time()

    light_oj_log_in(handle, passwd)

    time.sleep(waitTime)
    passwordBox = driver.find_element_by_xpath('//*[@id="mytable2"]/tbody/tr[3]/td/input')
    passwordBox.send_keys(passwd)
    driver.find_element_by_name('submit').click()

    time.sleep(waitTime)

    submissions = driver.find_elements_by_tag_name('tr')
    del submissions[0]
    del submissions[0]
    submissions.pop()

    submissions_ids = []
    file_names = []
    ext_types = []

    if not os.path.exists(handle):
        os.makedirs(handle)

    already_downlaod = GetDownloadedFile(handle)
    downloaded = ""

    for submission in submissions:
        WebDriverWait(submission, 30).until(expected_conditions.element_to_be_clickable((By.TAG_NAME, 'th')))
        submission_id = submission.find_element_by_tag_name('th').find_element_by_tag_name('a').text
        tds = submission.find_elements_by_tag_name('td')

        if tds[4].text == "-" or tds[5].find_element_by_tag_name('div').text != "Accepted" \
                              or submission_id in already_downlaod:
            continue

        title = tds[1].find_element_by_tag_name('a').text
        ext = get_ext(tds[2].text)
        file = handle + "/" + title + "_" + submission_id + "." + ext

        submissions_ids.append(submission_id)
        file_names.append(file)
        ext_types.append(ext)
        print(submission_id)

    for index, submission_id in enumerate(submissions_ids):
        driver.get(CODE_URL.format(submissionId=submission_id))
        WebDriverWait(driver, 30).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, ext_types[index])))
        elem = driver.find_element_by_class_name(ext_types[index])

        codes = elem.text
        # print(codes)
        fileName = file_names[index]

        downloaded += submission_id
        downloaded += "\n"

        with open(fileName, "w") as fp:
            tmp = ""
            for codeLetter in codes:
                if codeLetter == "\n":
                    codeLine = parse(tmp) + "\n"
                    fp.write(codeLine)
                    tmp = ""
                    continue
                tmp += codeLetter

            if len(tmp) > 0:
                codeLine = parse(tmp) + "\n"
                fp.write(codeLine)
                tmp = ""

        time.sleep(2)

    SetDownloadedFile(handle, downloaded)
    driver.quit()
    end_time = time.time()
    print("\n\nSuccessfully Completed 100%")
    print('Execution time %d seconds' % int(end_time - start_time))


if __name__ == "__main__":
    main()