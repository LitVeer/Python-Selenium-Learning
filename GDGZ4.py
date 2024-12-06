# -*- coding: UTF-8 -*-
import time, sys, os, requests
import paramiko
import switch as switch
from datetime import datetime, timedelta, timezone
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service


#驱动检查模块
def check_chromedriver_exists():
    possible_paths = [
        # "C:/chromedriver.exe",
        # "/path/to/chromedriver",  # 可能的路径1
        # "/usr/local/bin/chromedriver",  # 可能的路径2
        # "C:/Program Files/ChromeDriver/chromedriver.exe",  # 可能的路径3（Windows）
        "./chromedriver.exe"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return Service(path)
    
    print("ChromeDriver 文件不存在.")
    input("按任意键退出...")
    sys.exit()


#限制模块
def get_network_time():
    try:
        response = requests.get("http://worldtimeapi.org/api/ip")
        data = response.json()
        network_time = datetime.fromisoformat(data['datetime'].replace('Z', '+00:00')).astimezone(timezone.utc)
        return network_time
    except Exception as e:
        print("脚本异常，请检查网络后重试")
        input("按任意键退出...")
        sys.exit()
        return None
def Limit():
    network_time = get_network_time()
    if network_time:
        local_time = fixed_local_time  # 使用固定的本地时间
        
        # 比较网络时间和本地时间
        time_difference = network_time - local_time
        if time_difference > timedelta(seconds=0):
            print("脚本已过期，请联系相关人员更新")
            input("按任意键退出...")
            sys.exit()
        else:
            return None
    else:
        print("脚本异常，请检查网络后重试")
        input("按任意键退出...")
        sys.exit()

#登录模块
def login(driver, username, password, url):
    try:
        #访问天翼云，并进行登录 https://www.ctyun.cn/
        driver.get(url)
        print('正在访问...')
    except Exception as e:
        print('访问异常，请检查网络！')

    try:
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div[2]').click()
        driver.find_elements(By.CLASS_NAME, 'el-input__inner')[0].send_keys(username)
        driver.find_elements(By.CLASS_NAME, 'el-input__inner')[1].send_keys(password)
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div/form/div[3]/div/label/span[1]/span').click()
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div/form/div[4]/button').click()
        print('登录中...')
    except Exception as e:
        print('登录异常，请检查账号密码！')


#ECS购买模块_GDGZ4
def ECS_buy_GDGZ4(driver, actions, username, password, ecs_password):
    try:
        login(driver, username, password, 'https://console2.ctyun.cn/ecm/?region=cn-gdgz1&locale=zh-CN#/ecs/createVm')


        #选择区域
        driver.find_element(By.XPATH, '//*[@id="az_button_button_az0"]/span').click()


        #选择服务器
        time.sleep(1)
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ecs-flavor-search-id_input"]')))
        driver.find_element(By.XPATH, '//*[@id="ecs-flavor-search-id_input"]').send_keys('s7n')
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ecs-flavor-search-id_search"]')))
        driver.find_element(By.XPATH, '//*[@id="ecs-flavor-search-id_search"]').click()
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="fixedFlavorTable"]/table/tbody/tr[1]/td[1]')))
        driver.find_element(By.XPATH, '//*[@id="fixedFlavorTable"]/table/tbody/tr[1]/td[1]').click()


        #选择操作系统
        time.sleep(2)
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="platform_dominator_input"]/section/span')))

        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH, '//*[@id="platform_dominator_input"]/section/span'))
        actions.move_to_element(driver.find_element(By.XPATH, '//*[@id="platform_dominator_input"]/section/span')).click().perform()
        time.sleep(1)
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="platform_droplist_list_1"]')))
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH, '//*[@id="platform_droplist_list_1"]'))
        actions.move_to_element(driver.find_element(By.XPATH, '//*[@id="platform_droplist_list_1"]')).click().perform()


        #选择系统版本
        time.sleep(1)
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="imageModel_dominator_input"]/section/span')))
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH, '//*[@id="imageModel_dominator_input"]/section/span'))
        actions.move_to_element(driver.find_element(By.XPATH, '//*[@id="imageModel_dominator_input"]/section/span')).click().perform()
        time.sleep(1)
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="imageModel_droplist_list_1"]/section/span')))
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH, '//*[@id="imageModel_droplist_list_1"]/section/span'))
        actions.move_to_element(driver.find_element(By.XPATH, '//*[@id="imageModel_droplist_list_1"]/section/span')).click().perform()


        #关闭防护
        time.sleep(1)
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="hssRadioUnused_radio"]/span[1]')))
        driver.find_element(By.XPATH, '//*[@id="hssRadioUnused_radio"]/span[1]').click()


        #进行网络配置
        time.sleep(1)
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="toNetwork"]')))
        driver.find_element(By.XPATH, '//*[@id="toNetwork"]').click()


        #分配主机IP
        time.sleep(1)
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="allocate_dominator_btn"]')))
        driver.find_element(By.XPATH, '//*[@id="allocate_dominator_btn"]').click()
        time.sleep(0.5)
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="allocate_droplist_list_1"]/section/span')))
        driver.find_element(By.XPATH, '//*[@id="allocate_droplist_list_1"]/section/span').click()
        time.sleep(0.5)
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ipSectionGroup_input_3"]')))
        driver.find_element(By.XPATH, '//*[@id="ipSectionGroup_input_3"]').clear()
        driver.find_element(By.XPATH, '//*[@id="ipSectionGroup_input_3"]').send_keys(0)


        #修改安全组
        time.sleep(0.5)
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ecsCreateSecGroupReload"]')))
        actions.move_to_element(driver.find_element(By.XPATH, '//*[@id="ecsCreateSecGroupReload"]')).click().perform()
        time.sleep(0.5)
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="securityGroup_dominator_tag0_closeicon"]')))
        actions.move_to_element(driver.find_element(By.XPATH, '//*[@id="securityGroup_dominator_tag0_closeicon"]')).click().perform()
        time.sleep(0.5)
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="securityGroup_dominator_btn"]')))
        actions.move_to_element(driver.find_element(By.XPATH, '//*[@id="securityGroup_dominator_btn"]')).click().perform()
        time.sleep(0.5)
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="securityGroup_droplist_list_1"]/section/label')))        #选择端口全放开
        actions.move_to_element(driver.find_element(By.XPATH, '//*[@id="securityGroup_droplist_list_1"]/section/label')).click().perform()
        print('端口放开')
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="toConfig"]')))       #确认
        driver.find_element(By.XPATH, '//*[@id="toConfig"]').click()


        #输入密码
        time.sleep(1)
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="confirmPassword"]')))
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="toConfirm"]')))
        driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(ecs_password)
        driver.find_element(By.XPATH, '//*[@id="confirmPassword"]').send_keys(ecs_password)
        driver.find_element(By.XPATH, '//*[@id="toConfirm"]').click()


        #确认配置
        time.sleep(2)
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="protocolCheckBox_checkbox"]/span[1]')))
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="confirmOrder"]')))
        actions.move_to_element(driver.find_element(By.XPATH, '//*[@id="protocolCheckBox_checkbox"]/span[1]')).click().perform()
        driver.find_element(By.XPATH, '//*[@id="confirmOrder"]').click()


        #支付
        time.sleep(2)
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[4]/div/div[2]/div[2]/button')))
        time.sleep(5)
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[4]/div/div[2]/div[2]/button').click()
        time.sleep(10)
        print("购买ECS成功--广州4")
    except Exception as e:
        print("购买ECS失败，请手动检查订单")
        print('\n',e)
        input('按任意键退出...')
        sys.exit()


#IP购买模块_GDGZ4
def IP_Buy_GDGZ4(driver, username, password):
    #购买IP https://console2.ctyun.cn/vpc/?region=cn-gdgz1#/eip/eips/list
    try:
        #登录购买页面
        login(driver, username, password, 'https://console2.ctyun.cn/vpc/?region=cn-gdgz1#/eip/eips/list')
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="eip-create"]')))
        driver.find_element(By.XPATH, '//*[@id="eip-create"]').click()
        print("正在购买IP...")


        #进行购买
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="billType_button_button_1"]/span')))
        driver.find_element(By.XPATH, '//*[@id="billType_button_button_1"]/span').click()
        time.sleep(1)
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.TAG_NAME, 'tp-selectitem')))
        driver.find_elements(By.TAG_NAME, 'tp-selectitem')[1].click()
        
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME, 'ti3-spinner-input-box')))
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="BuyNumSpin_spinner_input"]')))
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, 'ti3-spinner-input-box').find_element(By.TAG_NAME, 'input').clear()
        driver.find_element(By.CLASS_NAME, 'ti3-spinner-input-box').find_element(By.TAG_NAME, 'input').send_keys(20)
        driver.find_element(By.XPATH, '//*[@id="BuyNumSpin_spinner_input"]').clear()
        driver.find_element(By.XPATH, '//*[@id="BuyNumSpin_spinner_input"]').send_keys(10)
        time.sleep(5)
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="buyImmediatelyBtn"]')))
        driver.find_element(By.XPATH, '//*[@id="buyImmediatelyBtn"]').click()


        #确认购买
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.TAG_NAME, 'ti-item')))
        print('购买地区：', driver.find_element(By.TAG_NAME, 'basic-info-config-render').find_elements(By.TAG_NAME, 'ti-item')[0].find_element(By.TAG_NAME, 'div').text,'\n')
        
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.TAG_NAME, 'ibiza-vpc-service-agreement')))
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="submitBtn"]')))
        driver.find_element(By.TAG_NAME, 'ibiza-vpc-service-agreement').find_elements(By.TAG_NAME, 'td')[2].find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME, 'label').click()
        driver.find_element(By.XPATH, '//*[@id="submitBtn"]').click()
    except Exception as e:
        print("购买IP失败，请手动检查订单")
        print('\n',e)
        input('按任意键退出...')
        sys.exit()
  

#控制台修改模块_General
def Console_Setting(driver, actions, username, password, selection):
    #控制中心部署
    try:
        #进入控制中心
        login(driver, username, password, 'https://console2.ctyun.cn/console/?region=cn-gdgz1#/home')
        driver.find_element(By.XPATH, '//*[@id="cf-service-sidebar"]/cf-sidebar/div/cf-new-collection/ul/li[1]/a/span[1]/i').click()
        driver.find_element(By.XPATH, '//*[@id="name_link_0"]').click()


        #绑定弹性ip
        if(selection == '0' or selection == 'a'):
            try:
                print("正在绑定弹性ip...")
                actions.move_to_element(driver.find_element(By.XPATH, '//*[@id="ecsDetailTabs_list"]/li[5]')).click().perform()
                driver.find_element(By.XPATH, '//*[@id="ecs-detail-bind-eip-button"]').click()
                
                #切换绑定弹性ip面板
                time.sleep(1)
                #driver.switch_to.frame('eipWidgetWin')
                #绑定
                actions.move_to_element(driver.find_elements(By.CLASS_NAME, 'ti3-radio-skin')[0]).click().perform()
                driver.find_element(By.XPATH, '//*[@id="ecs_detail_unBindEip_confirm_button"]').click()
            except Exception as e:
                print("绑定弹性ip错误，请手动检查")
                print('\n',e)
                input('按任意键退出...')
                sys.exit()


        #创建虚拟IP
        if(selection == '0' or selection == 'a' or selection == 'b'):
            try:
                print("正在创建虚拟IP...")
                time.sleep(20)
                actions.move_to_element(driver.find_element(By.XPATH, '//*[@id="ecsDetailTabs_list"]/li[3]')).click().perform()
                time.sleep(10)
                driver.refresh()
                driver.find_element(By.XPATH, '//*[@id="nicActionMenu0_managePrivateIp"]').click()
                driver.switch_to.window(driver.window_handles[-1])
                
                for i in range(1,10):
                    driver.find_element(By.XPATH, '//*[@id="create-event"]').click()
                    #driver.switch_to.frame('//*[@id="create-vip-modal"]')
                    driver.find_element(By.XPATH, '//*[@id="vipAssignMode_button_button_1"]').click()
                    driver.find_element(By.NAME, 'input_3').send_keys(i)
                    driver.find_element(By.CLASS_NAME, 'ti3-modal-footer').find_element(By.TAG_NAME, 'button').click()
                    print("创建虚拟IP: 192.168.0.1%d"%i)
                    time.sleep(5)
            except Exception as e:
                print("创建虚拟ip错误，请手动检查")
                print('\n',e)
                input('按任意键退出...')
                sys.exit()    
            

        #绑定IP
        if(selection == '0' or selection == 'a' or selection == 'b' or selection == 'c'):
            try:
                try:
                    actions.move_to_element(driver.find_element(By.XPATH, '//*[@id="ecsDetailTabs_list"]/li[3]')).click().perform()
                    driver.find_element(By.XPATH, '//*[@id="nicActionMenu0_managePrivateIp"]').click()
                    driver.switch_to.window(driver.window_handles[-1])
                except:
                    None

                print("正在绑定虚拟IP...")
                for i in range(9):
                    driver.find_element(By.XPATH, '//*[@id="vip-list_bind-eip-event_%d"]'%i).click()
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ag-selection-checkbox')))
                    actions.move_to_element(driver.find_element(By.ID, 'ibiza-vpc-vip-bind-eip').find_element(By.CLASS_NAME, 'ag-center-cols-container')
                                            .find_elements(By.TAG_NAME, 'input')[0]).click().perform()
                    driver.find_element(By.CLASS_NAME, 'ti3-modal-footer').find_element(By.TAG_NAME, 'button').click()
                    time.sleep(5)
            except Exception as e:
                print("绑定弹性ip错误，请手动检查")
                print('\n',e)
                input('按任意键退出...')
                sys.exit() 


        #绑定实例
        if(selection == '0' or selection == 'a' or selection == 'b' or selection == 'c' or selection == 'd'):
            try:
                print("\n正在绑定实例...")    
                try:
                    actions.move_to_element(driver.find_element(By.XPATH, '//*[@id="ecsDetailTabs_list"]/li[3]')).click().perform()
                    driver.find_element(By.XPATH, '//*[@id="nicActionMenu0_managePrivateIp"]').click()
                    driver.switch_to.window(driver.window_handles[-1])
                except:
                    None

                for i in range(9):
                    driver.find_element(By.XPATH, '//*[@id="vip-list_bind-vm-event_%d"]'%i).click()
                    
                    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ag-selection-checkbox')))
                    
                    #print(driver.find_element(By.ID, 'ibiza-vpc-vip-bind-vm').find_element(By.CLASS_NAME, 'ag-center-cols-container'))
                    actions.move_to_element(driver.find_element(By.ID, 'ibiza-vpc-vip-bind-vm').find_element(By.CLASS_NAME, 'ag-center-cols-container')
                                            .find_elements(By.TAG_NAME, 'input')[0]).click().perform()
                    
                    driver.find_element(By.CLASS_NAME, 'ti3-modal-footer').find_element(By.TAG_NAME, 'button').click()
                    time.sleep(5)
            except Exception as e:
                print("绑定实例错误，请手动检查")
                print('\n',e)
                input('按任意键退出...')
                sys.exit() 
            

        #获取主机IP
        driver.find_element(By.XPATH, '//*[@id="cf-collections-ecm"]/a/span[1]/i').click()
        main_ip = driver.find_element(By.XPATH, '//*[@id="eip_third_link_0"]').text
        
        return main_ip
    except Exception as e: 
        print("部署失败，请手动检查")
        print('\n',e)
        input('按任意键退出...')
        sys.exit()


#SSH模块
def send_files_to_linux(local_directory, remote_host, remote_port, remote_username, remote_password, remote_directory):
    # SSH连接参数
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 连接到远程主机
        ssh_client.connect(remote_host, port=remote_port, username=remote_username, password=remote_password)

        # 使用SCP将文件发送到远程主机
        with paramiko.SFTPClient.from_transport(ssh_client.get_transport()) as sftp:
            # 遍历本地文件夹下的所有文件
            for root, dirs, files in os.walk(local_directory):
                for file in files:
                    local_file_path = os.path.join(root, file)
                    remote_file_path = os.path.join(remote_directory, file)
                    # 获取本地文件大小
                    local_file_size = os.stat(local_file_path).st_size
                    # 将本地文件发送到远程主机
                    with tqdm(total=local_file_size, unit='B', unit_scale=True, desc=f"传输 {file}") as pbar:
                        def callback(sent, total):
                            pbar.update(sent - pbar.n)

                        sftp.put(local_file_path, remote_file_path, callback=callback)
                    print(f"文件 '{local_file_path}' 发送到 '{remote_host}:{remote_file_path}' 成功。")

    except paramiko.AuthenticationException:
        print("身份验证失败，请验证您的凭据。")
    except paramiko.SSHException as e:
        print("无法建立SSH连接: ", str(e))
    finally:
        # 关闭SSH连接
        ssh_client.close()

def execute_ssh_commands(remote_host, remote_port, remote_username, remote_password, command):
    # SSH连接参数
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 连接到远程主机
        ssh_client.connect(remote_host, port=remote_port, username=remote_username, password=remote_password)

        # 执行SSH命令
        stdin, stdout, stderr = ssh_client.exec_command(command)

        # 实时输出命令执行结果
        for line in iter(stdout.readline, ""):
            print(line, end="")

        # 打印命令执行结果
        print("标准错误:")
        print(stderr.read().decode())

    except paramiko.AuthenticationException:
        print("身份验证失败，请验证您的凭据。")
    except paramiko.SSHException as e:
        print("无法建立SSH连接: ", str(e))
    finally:
        # 关闭SSH连接
        ssh_client.close()

if __name__ == '__main__':

    # 设置固定的本地时间，并加上时区信息
    fixed_local_time = datetime(2024, 12, 5, 0, 0, 0, tzinfo=timezone.utc)
    #Limit()

    #检查驱动
    service = check_chromedriver_exists()

    #获取账号密码
    username = input('请输入账号：')   
    password = input('请输入密码：')     
    ecs_password = input("请输入ECS密码：")
    selection_0 = input("全局部署【0】  局部部署【1】\n")
    
    #测试
    username = "test"   
    password = "test"     
    ecs_password = "test"
    
    #Chrome浏览器
    option = webdriver.ChromeOptions()
    # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    option.add_argument("--headless")
    # 谷歌文档提到需要加上这个属性来规避bug
    option.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.implicitly_wait(15)
    actions = ActionChains(driver)
    
    #运行
    if(selection_0 == '0'):
        IP_Buy_GDGZ4(driver, username, password)      #IP购买
        time.sleep(3)
        ECS_buy_GDGZ4(driver, actions, username, password, ecs_password)      #ECS购买
        time.sleep(3)
        ip = Console_Setting(driver, actions, username, password, '0')        #控制台部署
    if(selection_0 == '1'):
        selection_1 = input("IP购买【1】        ECS购买【2】       控制台部署【3】\n")
        if(selection_1 == '1'):
            IP_Buy_GDGZ4(driver, username, password)
        if(selection_1 == '2'):
            ECS_buy_GDGZ4(driver, actions, username, password, ecs_password)
        if(selection_1 == '3'):
            selection_2 = input("全局部署【0】      绑定IP(主机)【a】      创建虚拟IP【b】     绑定IP【c】       绑定实例【d】\n")
            ip = Console_Setting(driver, actions, username, password, selection_2)

    #打印主机IP、账户名、密码
    print('主机IP：', ip)
    print('ECS账户名：root')
    print('ECS密码：', ecs_password)

    input('请保存主机IP、ECS密码，回车进入SSH连接...')

    #SSH连接
    if(selection_0 == '0' or (selection_0 == '1' and selection_1 == '3')):
        # 远程主机信息
        remote_host = ip
        remote_port = 22  # 默认的SSH端口号是22
        remote_username = 'root'

        # 本地文件夹路径
        local_directory = './ssh'

        # 远程目录
        remote_directory = '/root/'

        # 要执行的命令
        command = 'chmod +x * && ./auto.sh'
        for i in range(2):
            # 从用户输入获取密码
            remote_password = input(f"请输入 {remote_username}@{remote_host} 的密码: ")

            # 发送文件到远程主机
            send_files_to_linux(local_directory, remote_host, remote_port, remote_username, remote_password, remote_directory)

            # 执行SSH命令并实时获取输出
            print("\n\n配置时间较久，请耐心等待...")
            execute_ssh_commands(remote_host, remote_port, remote_username, remote_password, command)
    
        print('主机IP：', ip)
        print('ECS账户名：root')
        print('ECS密码：', ecs_password)
        
    input('按任意键退出...')