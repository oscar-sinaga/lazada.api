import hashlib
import requests
import json
from datetime import datetime as dt
import re

class Tokopedia(object):
    def getItems(self,query,page):
        url = "https://gql.tokopedia.com/"

        payload = json.dumps([
            {
            "operationName": "SearchProductQueryV4",
            "variables": {
                "params": f"device=desktop&city=257&navsource=home&ob=23&start={page}&pages=1&q={query}&related=true&rows=50&safe_search=false&scheme=https&shipping=&source=search&st=product&unique_id=9a19707053bb683135197ad2cdaa9b44&user_id=4130448&variants="
            },
            "query": "query SearchProductQueryV4($params: String!) {\n  ace_search_product_v4(params: $params) {\n    header {\n      totalData\n      totalDataText\n      processTime\n      responseCode\n      errorMessage\n      additionalParams\n      keywordProcess\n      __typename\n    }\n    data {\n      isQuerySafe\n      ticker {\n        text\n        query\n        typeId\n        __typename\n      }\n      redirection {\n        redirectUrl\n        departmentId\n        __typename\n      }\n      related {\n        relatedKeyword\n        otherRelated {\n          keyword\n          url\n          product {\n            id\n            name\n            price\n            imageUrl\n            rating\n            countReview\n            url\n            priceStr\n            wishlist\n            shop {\n              city\n              isOfficial\n              isPowerBadge\n              __typename\n            }\n            ads {\n              id\n              productClickUrl\n              productWishlistUrl\n              shopClickUrl\n              productViewUrl\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      suggestion {\n        currentKeyword\n        suggestion\n        suggestionCount\n        instead\n        insteadCount\n        query\n        text\n        __typename\n      }\n      products {\n        id\n        name\n        ads {\n          id\n          productClickUrl\n          productWishlistUrl\n          productViewUrl\n          __typename\n        }\n        badges {\n          title\n          imageUrl\n          show\n          __typename\n        }\n        category: departmentId\n        categoryBreadcrumb\n        categoryId\n        categoryName\n        countReview\n        discountPercentage\n        gaKey\n        imageUrl\n        labelGroups {\n          position\n          title\n          type\n          __typename\n        }\n        originalPrice\n        price\n        priceRange\n        rating\n        shop {\n          id\n          name\n          url\n          city\n          isOfficial\n          isPowerBadge\n          __typename\n        }\n        url\n        wishlist\n        sourceEngine: source_engine\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
            }
        ])
        headers = {
            'Content-Type': 'application/json',
            'Cookie': '_abck=A394DB445EE1B4C37902448775049D8C~-1~YAAQ3KwwF2fplVaDAQAAick6eQi6Ntuh8dbfC+g7WYqz/YYIzwXwUJ/bVVVwq2NLNFuri+tdM5TrhCOm5cGeFbgFnhNS9RuP8RHiY7SPGVHoEuSax117Qxipb74y0CGrASu4cNYMJ1bPIVPmxvuMDrPL6JIMHpuqPcwdwGi8sJUchzl/UtYNIff10F5/IsMEVI1VC+Y21XJJveqaIRTG9gC1FBcgtikccFg2sDbTDAc3Ouy/jncUP28YiZxVjadF/5kc2GU7tqqCQxByHqqMFf9oWA19GIjKOnC4NOMWM1fgXsEOwvKMedZgraqqunU1CdePZYi9m9HRO4FeYumKOi6N4VroTBm4VM1Vssxz3YiozKsybc9aP9JaEb4=~-1~-1~-1; bm_sz=350066C2D131BBA40ED9E729F426D046~YAAQ3KwwF2jplVaDAQAAick6eRFwKjBHuirXMaUJxmomQ/XXNAZuxrfut0YGY9ct+c8H1EyT9/KSOw7hSaa3OYIJzh8Look4ISrY2aKmehX4OiEoWgxWlTzxNi+PHbRYEzMFi+WgVeCFBTQLHTupsaLwyn+MnINDLtbUqd0gaBK1Ila+NSz0cmDPML6oTnHK9u48eDj6Gmoe+xjDvk+NPGcCpUMzMW6j2lTIWdflFwpC/Haps5Deb4nHDDfJrcO+3JgN6LxIX/PDG0j+k1p3g83kCASU44VnvlR4r6E2Bvb6PsOLaAU=~3356723~3618870'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        result = response.json()[0]

        data = result['data']['ace_search_product_v4']

        return data

    def getDetail(self,url):
        regex = re.search(r".+/(.+)/(.+)",url)
        shop_domain = regex[1]
        product_key = regex[2]

        url = "https://gql.tokopedia.com/graphql/PDPGetLayoutQuery"

        payload = json.dumps([
            {
            "operationName": "PDPGetLayoutQuery",
            "variables": {
                "shopDomain": shop_domain,
                "productKey": product_key,
                "layoutID": "",
                "apiVersion": 1
            }
            }
        ])
        headers = {
            'authority': 'gql.tokopedia.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'cookie': '_UUID_NONLOGIN_=e9727c37c5f733a77479185a66e63e4d; _UUID_NONLOGIN_.sig=tkAjvTdngH8Tn2TawWMZs8yir7g; DID=a717cbd11e2c1799009d1f87dd469aee95e922f0f927d3df40966a41e4eec18f634c74b0f2242b80393e711af4bf7119; DID_JS=YTcxN2NiZDExZTJjMTc5OTAwOWQxZjg3ZGQ0NjlhZWU5NWU5MjJmMGY5MjdkM2RmNDA5NjZhNDFlNGVlYzE4ZjYzNGM3NGIwZjIyNDJiODAzOTNlNzExYWY0YmY3MTE547DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=; __auc=f6d4b66f17cefc7db9583cc0ea3; _hjid=52f6214b-1f92-4aac-a3be-adc11e04aafc; cto_bundle=T0m1vF83VlNReTd2VXh6JTJGdGNtNXhZUDZMbkQ3WjZveUxUM1ZVUHdkd3FKcSUyQlNTMUclMkJtZHpDdyUyRllUU0x3ZWlHWHJGT2dIWWQ4WTdqejBxSTNJWFMwMGMlMkZHVXJuUWUyZG9VaDRlblczS0F5TWhJM0YzN2VRdDhwS3UlMkZzV2clMkYxRTlpczRXaWt3Z0xMbWJqbEhtZFg4VlFWV1ZmQSUzRCUzRA; _UUID_CAS_=cc18f322-9a5c-4cf6-9dfd-1270e46f8582; _CASE_=732a6c416c2a3238242a69416c2a3238242a646a642a322a2a242a6b416c2a3238242a6467666f2a322a2a242a64697c2a322a2a242a784b672a322a2a242a7f416c2a32393a3a39383b3f3d242a7b416c2a3239393d3b383d3f3b242a7b5c71786d2a322a3a602a242a7f607b2a322a5373542a7f697a6d60677d7b6d57616c542a32393a3a39383b3f3d24542a7b6d7a7e616b6d577c71786d542a32542a3a60542a24542a57577c71786d6669656d542a32542a5f697a6d60677d7b6d7b542a752473542a7f697a6d60677d7b6d57616c542a323824542a7b6d7a7e616b6d577c71786d542a32542a393d65542a24542a57577c71786d6669656d542a32542a5f697a6d60677d7b6d7b542a75552a75; _gcl_au=1.1.1070690307.1661094594; _jxx=74cb82d0-f38f-11ec-b88d-977b36f46df7; _jx=74cb82d0-f38f-11ec-b88d-977b36f46df7; hfv_banner=true; bm_sz=FEDD193B43C05ABC0ECC7F218FD5E1C0~YAAQrSE1F/1cP+SDAQAA9oK15BF3DdkWy7nnyvTZieay5zJg128l/5uxqPSqkvFazOh4Wv3W/4AUQLS9ZTkA7gC6IWSGdmyUZZDpZneKXHpnw0z91FQk9Ydt+eYC27M4tsYrzfda+aWzsuJrefZsvvOvug/ZvrS4RI1pFjgoeAaotUY3gVVJBEa7KCQis4W/5OO94n03wgyxu7fB1vq8Gve2bXtPMuOP9kc5ShEm/stdSNt9WjiVt4Yvg9TMEDMK/8UqBRsvXbD8YPvbYdWMUw12n/bq+LfTV2EPb8hs1YAkS1U8+IE=~3293746~3355201; _SID_Tokopedia_=699V7myhqHJTekLwfsmffoi8jhxDptrX0TwX7hPKexK0RauqTC_em34ZEmpLo2P4yP7P2bCiEz2ll3qvPtNZtHAc3ocJtX5BLZG8pSe5mP3NYlRhpiclF-cTdKOejSvt; _gid=GA1.2.750563175.1665989199; _jxxs=1665989198-74cb82d0-f38f-11ec-b88d-977b36f46df7; _jxs=1665989198-74cb82d0-f38f-11ec-b88d-977b36f46df7; __asc=c2c83db8183e4b1d556eeadc2a6; NR_SID=NRl9cf5q6os1xrv; AMP_TOKEN=%24NOT_FOUND; ak_bmsc=154ED6F998E215265D990C8CABCF4618~000000000000000000000000000000~YAAQrSE1F3NuP+SDAQAALge35BEb0jR/EDHlGS9fxmk/fhk3+qBfnzY2Jv4HxyBnR6N0LsUayf3aiZXy3bUvITnTC1ZgZmWsLLcdS2aqgATfgZVTpkFvW9tCgDV0L3fpPHYR3sGnhjtTirg4mfbGw+C3xEDjSn14AS7SNnN0aCgzZzX7e229gmZGfuOALcII9lwh7LwBRSSd/BSKyn3Y34PH7qqwOS+F624Xm9fNwbbMGdnadv9PfPteUhSC9U0cqgtDxE7pAjc8vewzIf2xm/cr0+dCN+s7shGPXDk+ELtFGKYgFyz1Sp1aOIs606S4hJpX/sTzXvLceppM0tJ66/vCIzwAJD4id/VwC3N1teNAly0yhb28sTe5lNA5RnTYE27j6cEAGLbKObWIzNyULaf3e2bv0o5utLMRpqGbApAoKvbDgOBPjF+rBxoKSoByJnxlCM98M0G9XAzxpRDnRFLujKTzZ8CKnMk9FrZpdbttHVJT9YTHic7TMHYIOsUgra67HX3PGg==; _abck=DB9B8AC184B53D64511C0CA8E46737CB~0~YAAQrSE1F9ZuP+SDAQAAKxG35AgWg2PHBBvM9/T36YC42lsBvwpdbpPSZABAxneyJL5ZbzE4lx5xlz2XwH9a8MQ5IfXHqhgsra6cBqqSzU8xgcNOFIlp7RMpBNfjV2Cwla2iNAzzdbmskpkIB8HqujKdWibzNMJpXB/YqmiZwj/FLyVR8kUpJo+UG0evJyaNil6vVqoXXUPQmUFSGAoArQTI8WXXlKanMKbaIh8xLxRgv1rt5kKf5/R1m6275w1fQfh83by6VurvHnEd0YDOndLmPJdXI8Piow/tMatTi3FNObNjmHg5CNA63K5yxPtTnJsl3kG1Wexk7cH4FFpG74EMGWHukQZ6IFpeUymcj52FjxWYPwAH0lEKNq/qdOibLir0JybgJeLz8xa1eN2kXLlo06yKOnEkUWDl~-1~-1~-1; _dc_gtm_UA-126956641-6=1; _ga_70947XW48P=GS1.1.1665989198.16.1.1665989428.60.0.0; _ga=GA1.2.426299726.1636110422; _dc_gtm_UA-9801603-6=1; _abck=DB9B8AC184B53D64511C0CA8E46737CB~-1~YAAQrSE1F6clQOSDAQAA8Z3F5AhK11JVGEv0Mwg28CHe7ro9JDkPKhPuivMf6GtvJC4Bk/p7zI4a2xBftcSFG9nLsyh8w7LWvqI9LXyIg8zU4rbbRPpp5yk+oCyh7u0KTSOM4XRJaXk2MKwIG+Irdo5rGB8e0UJy+dr6OsWCBl/bnTIXj2xIvqwKEbLiGyyNX+keTPXnqVhARZ/m0OmEUnreuuXiazWGwjCJMPeMd2H405ipu3hEEJYVDEaxMp+zpT1y3FqjjfgUkSzoISVkh2rF73Cpz4yYNfC0HQeI0E1mcDJjDcxXQjErIOkN1O5bcwK/fWpXcC7r9nWWyDUB8RJanaDewcwGelUaKbA6lOmoJwIuCK7ON8DQzweB4opfl/xTUD7GVBnTyxhavU1zs3G+FDX+9UwPAaOw~0~-1~-1; bm_sz=933FB20E8A08C7F904B2BBEFAF59CF75~YAAQrSE1F8lFP+SDAQAAGuez5BFT+bdQDJxSRM+CqoyWKuJfBc5YLC9LptyhgD3iV0UTDDXYfIRkrJDvV3Uec6IMyRTsdgAjoHmRZ7fcDgjn1ynK05v+6t+cnwthQS1mSNrX6pjpQXQ3GJYjyW4SOG/TxwhZdXe13s/IYVoT8wsqF3jE/zmnc+FRmDrDQRpll4sWG/F/nsWCuBmtRrbB9nuHCuLffgln81YTFV1rWA8koN7HsTzOhv8+t3U1tkERLb1/B4OIaNAiP777rxQXW1gXyC7PafPY98603/oT9yhiNBb1q1U=~4534576~3163705',
            'origin': 'https://www.tokopedia.com',
            'queryhash': 'v1:90338d207352e8b71cf754979b915218;false',
            'referer': 'https://www.tokopedia.com/miniso-official/miniso-sandal-rumah-slipper-wanita-selop-comfortable-nyaman-flip-flop-light-green-39-40?extParam=src%3Dmultiloc%26whid%3D7377294',
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36',
            'x-device': 'mobile',
            'x-source': 'tokopedia-lite',
            'x-tkpd-akamai': 'pdpGetLayout',
            'x-tkpd-lite-service': 'atreus',
            'x-version': '859a718'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        result = response.json()

        data = result[0]['data']['pdpGetLayout']

        return data

class Bukalapak(object):
    def __init__(self):
        url = "https://m.bukalapak.com/westeros_auth_proxies"

        payload = json.dumps({
            "application_id": 1,
            "authenticity_token": ""
            })
        headers = {
            'authority': 'm.bukalapak.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'cookie': 'identity=1434c9a07debe4ddd20136f1459c7b95; browser_id=4401cf84bbe62fc1cf824702c8b64c73; session_id=d75ecdf4d556622b6113a43f10cb7230; nlbi_2720203=02f1XCHQXUTBf1M0aKZlFQAAAAB7aCVMyDeogX/M9bmUS5AE; visid_incap_2720203=Uz2O0q2ZTGSQ/dsB6idsj2PuP2MAAAAAQUIPAAAAAAA2Gzj8y9OQNEuzr8772abE; incap_ses_7252_2720203=UvuYbpVPNTnsH4dqwkekZGPuP2MAAAAAgTDWT6rzem3nG0pUS3n4rA==; _gcl_au=1.1.550661893.1665133940; _gid=GA1.2.2143629744.1665133940; _dc_gtm_UA-12425854-1=1; _ga=GA1.2.1005518399.1665133940; _tt_enable_cookie=1; _ttp=1a92c0c1-34ef-4061-aec4-a524189dcfbb; _fbp=fb.1.1665133941036.205877771; nlbi_2720203_2147483392=e/cqe1dkKADq82fZaKZlFQAAAABJPaYxzzEf6xB3Ko+1Azsf; __asc=2dd48532183b1b79f46aef62e4e; __auc=2dd48532183b1b79f46aef62e4e; cto_bundle=DIQhI19ERnhCQ2E1SUZWbjlPZWQlMkZDJTJGRTVWc255V0ZSTTF3ZmJCSXJHTXIwdERhY1NCQk5NU2I2a0RsSktQNDclMkY0dU1GUWxob29YMlI0RWFibFp0dEN2MFFSVVdmNW1FY1JYaG1wdFlTOUFNZWFFRnRGMnFIbHolMkZmaEFWTE0wTHRtWU5E; _vid_t=fI+C22MkJq0W4ys/HAm3A/GU79vS49QWeK1jRYTPvCPbMcwLr/dzZgyVf0befhwgSj3LzvUIsONsjQ==; lskjfewjrh34ghj23brjh234=MzdINTA5clh6bWdHZTdNNHppQWdMNEM3VEJJNVJCYVQyQzlPeWR0emJJN1l1UTc3TGk4NFFYK1MxeDVrai9TeG0zdEpBQTl5cWkrVCtuL2tDdGUwUmc9PS0tZm5KYkZEUHVvSGh5VUg3bkFYdXVSdz09--c8b1a9967604cc65150df8ee52c6bd2211e02ed0; nlbi_2720206=19sqF+sKayiBMjJwRICB2wAAAADRqxAlQ9grNH2Y5g6uglaG; visid_incap_2720206=ayMCX8ZiS+SQLD3RZSh6BW7uP2MAAAAAQUIPAAAAAADvFWTJo526lsEsxKdWYDZk; incap_ses_7252_2720206=uFBHCQI4zjDROYdqwkekZG7uP2MAAAAAPj6+Y5WfiluvS0sJTcbzVQ==; _ga_R2T40V5QM5=GS1.1.1665133940.1.0.1665133950.50.0.0; nlbi_2720206_2147483392=qsZ0FKZmZQ7QR0gVRICB2wAAAAA3J15olnyF8RxFZhgU2ze8; external_visit_tracker_marketplace={%22referrer%22:%22https://www.google.com/%22%2C%22url%22:%22https://m.bukalapak.com/%22%2C%22max_ages%22:%222022-10-07T09:42:31.191Z%22}; incap_ses_7252_2720185=jMMeNLPUmQ+GD3NqwkekZNnlP2MAAAAALx1oU76TkHoyxEM7QvlsSg==; lskjfewjrh34ghj23brjh234=T2FTYUhyNGdZdWRYTXFPZDRXRTVJTStUK29TZnlDdDh1aXViUE5IYkpsR1VsNkljWE1XNjhkZHBuMDQ5K2E0WVhGUWxzU09JaTJoNDd4ODJ1eS8rNHc9PS0tTDllb0N0SVlsckZKdVlqbWZ6eXBrUT09--9f042ae1a2edd784ea16d1b709e5ef398d90a425; nlbi_2720185=IuOJN0eYcDpRY5FdAkoPxgAAAAC9kFvUINxRo0qW52V8MaSk; nlbi_2720185_2658675=Z5+UcknfPxxMCb0KAkoPxgAAAACfkcn0taZmqRUUyNvvNV70; session_id=28174d0b7f81927104b671f7e8d1ece7; visid_incap_2720185=VPMBpMshRryB6LvnfAJyhEqKMWMAAAAAQUIPAAAAAAAnMhrF2CwGa+/xzEdzA8uq',
            'origin': 'https://m.bukalapak.com',
            'referer': 'https://m.bukalapak.com/',
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36'
            }

        response = requests.request("POST", url, headers=headers, data=payload)

        result = response.json()

        self.token = result['access_token']

    def getItems(self,keyword,page):
        url = f"https://api.bukalapak.com/multistrategy-products?keywords={keyword}&limit=50&offset=50&page={page}&facet=true&access_token={self.token}&prambanan_override=true"

        payload={}
        headers = {
        'Cookie': 'incap_ses_7252_2720185=jMMeNLPUmQ+GD3NqwkekZNnlP2MAAAAALx1oU76TkHoyxEM7QvlsSg==; lskjfewjrh34ghj23brjh234=T2FTYUhyNGdZdWRYTXFPZDRXRTVJTStUK29TZnlDdDh1aXViUE5IYkpsR1VsNkljWE1XNjhkZHBuMDQ5K2E0WVhGUWxzU09JaTJoNDd4ODJ1eS8rNHc9PS0tTDllb0N0SVlsckZKdVlqbWZ6eXBrUT09--9f042ae1a2edd784ea16d1b709e5ef398d90a425; nlbi_2720185=IuOJN0eYcDpRY5FdAkoPxgAAAAC9kFvUINxRo0qW52V8MaSk; nlbi_2720185_2658675=Z5+UcknfPxxMCb0KAkoPxgAAAACfkcn0taZmqRUUyNvvNV70; session_id=28174d0b7f81927104b671f7e8d1ece7; visid_incap_2720185=VPMBpMshRryB6LvnfAJyhEqKMWMAAAAAQUIPAAAAAAAnMhrF2CwGa+/xzEdzA8uq'
        }
    
        response = requests.request("GET", url, headers=headers, data=payload)

        result = response.json()

        return result

    def getDetail(self,url):
        regex = re.search(r".+/.+/(.+?)-",url)
        product_id = regex[1]
        url = f"https://api.bukalapak.com/products/{product_id}/?access_token={self.token}"

        payload={}
        headers = {
        'Cookie': 'incap_ses_7252_2720185=y/UrHILz2XxJvJVqwkekZIr0P2MAAAAAuY5zzhoOkDVzI4IIH4KTrw==; lskjfewjrh34ghj23brjh234=TC8zclQrMHdLb3JXQUpvTFJGKzRodGorbmEyRzdwWVZRSmR1djZuU29EQ3lIa1lhU1cwb1ArOHc1TFJ6aS95NEdxTHd4YnhSZGVrUStzZ2dlVjY5bGVtRGZNNlc2V1k4S09OL0k5M01ONlE9LS1qSTRuZHczY1FkWDlOMTZpTXFPYTRBPT0%3D--399b74ec686af086907a01fd3ab6df305bcad40c; nlbi_2720185=IuOJN0eYcDpRY5FdAkoPxgAAAAC9kFvUINxRo0qW52V8MaSk; nlbi_2720185_2658675=Z5+UcknfPxxMCb0KAkoPxgAAAACfkcn0taZmqRUUyNvvNV70; session_id=28174d0b7f81927104b671f7e8d1ece7; visid_incap_2720185=VPMBpMshRryB6LvnfAJyhEqKMWMAAAAAQUIPAAAAAAAnMhrF2CwGa+/xzEdzA8uq'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        result = response.json()

        return result['data']

class Lazada(object):
    def getItems(self,query,page):
        url = f"https://www.lazada.co.id/catalog/?_keyori=ss&ajax=true&from=input&isFirstRequest=true&page={page}&q={query}"

        payload={}
        headers = {
          'authority': 'www.lazada.co.id',
          'accept': 'application/json, text/plain, */*',
          'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
          'cookie': '__wpkreporterwid_=98884795-cebb-4cd4-2729-9290266a6194; hng=ID|id-ID|IDR|360; hng.sig=dJwrVwSueShOlZz95EBCvlH9FLAVtzGZ3msUnc25HIQ; lzd_cid=899e648d-6ba2-4a82-a3a4-c2dd4271313a; t_uid=899e648d-6ba2-4a82-a3a4-c2dd4271313a; _bl_uid=IUlI39ndk85lay4vn76R0jmlUapb; t_fv=1666483278536; cna=T3LbG+vYlhMCAbTyaSu9zrDz; _gcl_au=1.1.1640065967.1666918330; _fbp=fb.2.1666918338766.587895684; AMCV_126E248D54200F960A4C98C6%40AdobeOrg=-1124106680%7CMCIDTS%7C19294%7CvVersion%7C5.2.0%7CMCMID%7C80275101829536896263017449610910177661%7CMCAAMLH-1667525551%7C3%7CMCAAMB-1667525551%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1666927951s%7CNONE; sgcookie=E100%2BatxSEkTE%2BOd6CuD24yemzV3c%2B0ljSBn5drQGd%2FdMuUMEP6NmBydNVmbZJeGOjEed0m4Dr7x7AjGoR3igtV0uz4luBeb5zTesjsNCr9FJK0%3D; t_sid=19Vm7XTUOc44J3c1xjYL2WgUOEsAXKob; utm_origin=https://www.google.com/; utm_channel=SEO; _gcl_aw=GCL.1667033846.Cj0KCQjwnvOaBhDTARIsAJf8eVMYEO4BEjSd0DvIUPYpS0ZdzXanvnLg2AKvb319xEjYfCzJLliGBxoaAkl2EALw_wcB; lzd_sid=1887a2de6c7ad2c221bf42edf6b3d182; _m_h5_tk=4a9e3eb21b31be94a380ccd5162d0732_1667042126693; _m_h5_tk_enc=e2cd36a307c9a490ccd145eb98213583; _tb_token_=58eb68f56bea3; _uetsid=b9e3be90576711eda601d1bf5efa8301; _uetvid=c5c0b310565a11eda22f7136b4c07b0f; cto_bundle=YvY2LF9Xd2pqaFFHd050dGRXU1pxSWZWRER6VjNvTXYyOEZ4M00ydnZPRWo4OFl5emdjWXhETUNzUHRoSnpCQUNCWXloUFBWdkUwNk1PQW1MVzI3ODgzYjZ2dHRISWpVUHMxMkszNE0wSiUyQnNucmglMkJUSHNSbFQzc2pIZnFLdHlDV1R1NjdLNElHVnZibzB0UWxjS2U5ZU1LaCUyQlElM0QlM0Q; xlly_s=1; tfstk=cHlFBdfXpBdeEykhg5FrgUzXNaVdZuGoGpU8K3DCpb4hIPehiHj8SKxiv07NqJf..; l=eBO9PgPcTiQ7lsEFBOfZlurza77OSIRY6uPzaNbMiOCPOs1p5SjAW6ydrM89C3MNhsa6R3rp2umHBeYBqIDjLbHEAjH5SNDmn; isg=BIyMWkQKA4MJehf3EnBkmgh3Xeq-xTBvI-EQP-ZNmDfacSx7DtUA_4LHEWHJZmjH; hng=ID|id-ID|IDR|360; hng.sig=dJwrVwSueShOlZz95EBCvlH9FLAVtzGZ3msUnc25HIQ',
          'referer': 'https://www.lazada.co.id/catalog/?q=xiaomi&_keyori=ss&from=input&spm=a2o4j.home.search.go.41f753e0T41uYl',
          'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"',
          'sec-fetch-dest': 'empty',
          'sec-fetch-mode': 'cors',
          'sec-fetch-site': 'same-origin',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
          'x-csrf-token': '58eb68f56bea3',
          'x-requested-with': 'XMLHttpRequest'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        result = response.json()

        data = result['mods']['listItems']
        for item in data:
            item['url'] = f"https:{item['itemUrl']}"
            item['list_url'] = url
        
        return data
    
    def getDetail(self,url):
        payload={}
        headers = {
          'authority': 'www.lazada.co.id',
          'accept': 'application/json, text/plain, */*',
          'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
          'cookie': '__wpkreporterwid_=98884795-cebb-4cd4-2729-9290266a6194; hng=ID|id-ID|IDR|360; hng.sig=dJwrVwSueShOlZz95EBCvlH9FLAVtzGZ3msUnc25HIQ; lzd_cid=899e648d-6ba2-4a82-a3a4-c2dd4271313a; t_uid=899e648d-6ba2-4a82-a3a4-c2dd4271313a; _bl_uid=IUlI39ndk85lay4vn76R0jmlUapb; t_fv=1666483278536; cna=T3LbG+vYlhMCAbTyaSu9zrDz; _gcl_au=1.1.1640065967.1666918330; _fbp=fb.2.1666918338766.587895684; AMCV_126E248D54200F960A4C98C6%40AdobeOrg=-1124106680%7CMCIDTS%7C19294%7CvVersion%7C5.2.0%7CMCMID%7C80275101829536896263017449610910177661%7CMCAAMLH-1667525551%7C3%7CMCAAMB-1667525551%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1666927951s%7CNONE; sgcookie=E100%2BatxSEkTE%2BOd6CuD24yemzV3c%2B0ljSBn5drQGd%2FdMuUMEP6NmBydNVmbZJeGOjEed0m4Dr7x7AjGoR3igtV0uz4luBeb5zTesjsNCr9FJK0%3D; t_sid=19Vm7XTUOc44J3c1xjYL2WgUOEsAXKob; utm_origin=https://www.google.com/; utm_channel=SEO; _gcl_aw=GCL.1667033846.Cj0KCQjwnvOaBhDTARIsAJf8eVMYEO4BEjSd0DvIUPYpS0ZdzXanvnLg2AKvb319xEjYfCzJLliGBxoaAkl2EALw_wcB; lzd_sid=1887a2de6c7ad2c221bf42edf6b3d182; _m_h5_tk=4a9e3eb21b31be94a380ccd5162d0732_1667042126693; _m_h5_tk_enc=e2cd36a307c9a490ccd145eb98213583; _tb_token_=58eb68f56bea3; _uetsid=b9e3be90576711eda601d1bf5efa8301; _uetvid=c5c0b310565a11eda22f7136b4c07b0f; cto_bundle=YvY2LF9Xd2pqaFFHd050dGRXU1pxSWZWRER6VjNvTXYyOEZ4M00ydnZPRWo4OFl5emdjWXhETUNzUHRoSnpCQUNCWXloUFBWdkUwNk1PQW1MVzI3ODgzYjZ2dHRISWpVUHMxMkszNE0wSiUyQnNucmglMkJUSHNSbFQzc2pIZnFLdHlDV1R1NjdLNElHVnZibzB0UWxjS2U5ZU1LaCUyQlElM0QlM0Q; xlly_s=1; tfstk=cHlFBdfXpBdeEykhg5FrgUzXNaVdZuGoGpU8K3DCpb4hIPehiHj8SKxiv07NqJf..; l=eBO9PgPcTiQ7lsEFBOfZlurza77OSIRY6uPzaNbMiOCPOs1p5SjAW6ydrM89C3MNhsa6R3rp2umHBeYBqIDjLbHEAjH5SNDmn; isg=BIyMWkQKA4MJehf3EnBkmgh3Xeq-xTBvI-EQP-ZNmDfacSx7DtUA_4LHEWHJZmjH; hng=ID|id-ID|IDR|360; hng.sig=dJwrVwSueShOlZz95EBCvlH9FLAVtzGZ3msUnc25HIQ',
          'referer': 'https://www.lazada.co.id/catalog/?q=xiaomi&_keyori=ss&from=input&spm=a2o4j.home.search.go.41f753e0T41uYl',
          'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"',
          'sec-fetch-dest': 'empty',
          'sec-fetch-mode': 'cors',
          'sec-fetch-site': 'same-origin',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
          'x-csrf-token': '58eb68f56bea3',
          'x-requested-with': 'XMLHttpRequest'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        result = response.json()

        data = result['mods']['listItems']
        
        for item in data:
            item['url'] = f"https:{item['itemUrl']}"
        
        return data    
    