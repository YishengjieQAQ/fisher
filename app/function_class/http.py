import requests
class HTTP:
    '''发送request请求'''
    @staticmethod
    def get_url(url, return_json = True):
        r = requests.get(url)
        '''判断状态码以及判断ADI是否返回json'''
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text




