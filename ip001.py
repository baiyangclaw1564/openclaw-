import requests

def get_ip():
    try:
        return requests.get("https://api.ipify.org?format=json", timeout=5).json()["ip"]
    except:
        return None

def ping_test(ip):
    try:
        res = requests.get(f"https://ping0.cc/ip/{ip}", timeout=10)
        data = res.json()
        pings = [i["ping"] for i in data.get("data", []) if i.get("ping")]
        return sum(pings)/len(pings) if pings else None
    except:
        return None

def whoer_test():
    try:
        return requests.get("https://whoer.net/zh/main/api/ip", timeout=10).json()
    except:
        return {}

def isp_type(isp):
    if not isp:
        return "未知"
    isp = isp.lower()
    if any(x in isp for x in ["cloud","amazon","google","azure","aliyun"]):
        return "机房/云服务器"
    return "家庭/普通宽带"

def score_model(ping, anonymity, isp):
    score = 100
    if ping:
        if ping > 150: score -= 30
        elif ping > 100: score -= 20
        elif ping > 60: score -= 10
    if anonymity == "low": score -= 30
    elif anonymity == "medium": score -= 10
    if isp_type(isp) == "机房/云服务器": score -= 20
    return max(score, 0)

def analyze(score, ping, isp):
    if score < 60:
        print("❌ 当前网络环境较差")
    elif score < 80:
        print("⚠️ 网络环境一般")
    else:
        print("✅ 网络环境优秀")
    if isp_type(isp) == "机房/云服务器":
        print("⚠️ 检测到机房IP")
    if ping and ping > 100:
        print("⚠️ 延迟较高")

def main():
    print("🔍 openclaw 环境检测\n")
    ip = get_ip()
    if not ip:
        print("❌ 无法获取IP")
        return
    print("IP:", ip)
    ping = ping_test(ip)
    whoer = whoer_test()
    anonymity = whoer.get("anonymity")
    isp = whoer.get("isp")
    print("延迟:", round(ping,2) if ping else "未知")
    print("匿名度:", anonymity)
    print("ISP:", isp)
    print("类型:", isp_type(isp))
    score = score_model(ping, anonymity, isp)
    print("\n评分:", score)
    analyze(score, ping, isp)
    print("\n建议: 多地区 + 双ISP + 家庭网络")

if __name__ == "__main__":
    main()