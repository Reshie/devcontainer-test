from elasticsearch import Elasticsearch

es = Elasticsearch("http://elasticsearch:9200")

mapping = {
	"properties": {
		"title": {"type": "text"},
		"author": {"type": "text"},
		"views": {"type": "long"}
	}
}

es.indices.create(index="literature", body={"mappings": mapping})

doc = [
  	{
		"title": "〔雨ニモマケズ〕",
		"author": "宮沢 賢治",
		"views": 329655
  	},
  	{
		"title": "走れメロス",
		"author": "太宰 治",
		"views": 253431
  	},
  	{
		"title": "こころ",
		"author": "夏目 漱石",
		"views": 229964
  	},
  	{
		"title": "山月記",
		"author": "中島 敦",
		"views": 214078
  	},
  	{
		"title": "羅生門",
		"author": "芥川 竜之介",
		"views": 193606
  	},
  	{
		"title": "銀河鉄道の夜",
		"author": "宮沢 賢治",
		"views": 170405
  	},
  	{
		"title": "吾輩は猫である",
		"author": "夏目 漱石",
		"views": 158037
  	},
  	{
		"title": "夢十夜",
		"author": "夏目 漱石",
		"views": 135089
  	},
  	{
		"title": "やまなし",
		"author": "宮沢 賢治",
		"views": 132078
  	},
  	{
		"title": "人間失格",
		"author": "太宰 治",
		"views": 125129
  	},
]

for i, d in enumerate(doc):
	es.index(index="literature", id=i, body=d)

es.close()