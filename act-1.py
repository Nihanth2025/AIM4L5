import requests
import csv

url="https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"
token="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"
headers={"authorization": f"Bearer {token}"}
label_map={
    "LABEL_0": "Negative",
    "LABEL_1": "Neutral",
    "LABEL_2": "Positive"
}

def analyse_sentiment(text):
    try:
        response=requests.post(url, headers=headers, json={"inputs": text})
        if response.status_code !=200:
            return {"error" : f"API error {response.status_code}"}
        
        result=response.json()
        sorted_result=sorted(result[0], key=lambda x: x['score'], reverse=True)

        top_label=sorted_result[0]['label']
        top_score=sorted_result[0]['score']

        all_score={label_map.get(pred['label'], pred['label']): round(pred['score'],3) for pred in result[0]}

        return{
            "text": text,
            "sentiment": label_map.get(top_label, "Unknown"),
            "score": round(top_score,3),
            "all_scores":all_score
        } 
    except Exception as e:
        return {"error":str(e)}
    
texts=[
    "I fell good.",
    "The movie is neutral.",
    "It is terrible!",
    "It's sunny."
]

results=[]

for i in texts:
    a= analyse_sentiment(i)
    print(a)