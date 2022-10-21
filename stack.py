import requests, time, random, os, wp, githelper, sys, index
import datetime

path = os.path.dirname(sys.argv[0])
proxy_file = open( "./proxy2.txt", 'r')
proxy = proxy_file.readline().strip()

print ('Using proxy: ' + proxy)

os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy
os.environ['NO_PROXY'] = 'android.fixeme.com'
f = open('posts.txt', 'r')
posted_questions = f.read().split('\n')

tags = ['angular', 'android', 'android-studio', 'flutter', 'angularjs', 'c-language', 'css','HTML','laravel','ubuntu','linux','Unix', 'express', 'ghost-cms', 'git', 'ionic', 'javascript', 'linux', 'mysql', 'photoshop', 'php', 'python', 'django', 'flask', 'selenium', 'tensorflow', 'spring', 'typescript', 'windows','']
checkers = ['Laura B. (Easybugfix Admin)', 'Clifford M. (Easybugfix Volunteer)', 'David Marino (Easybugfix Volunteer)', 'Mildred Charles (Easybugfix Admin)', 'Gilberto Lyons (Easybugfix Admin)', 'Marie Seifert (Easybugfix Admin)', 'Marilyn (Easybugfix Volunteer)', 'Katrina (Easybugfix Volunteer)', ' Willingham (Easybugfix Volunteer)', 'Cary Denson (Easybugfix Admin)', 'Pedro (Easybugfix Volunteer)', 'Senaida (Easybugfix Volunteer)', 'Mary Flores (Easybugfix Volunteer)' , 'Terry (Easybugfix Volunteer)', 'David Goodson (Easybugfix Volunteer)', 'Timothy Miller (Easybugfix Admin)', 'Robin (Easybugfix Admin)', 'Candace Johnson (Easybugfix Volunteer)', 'Dawn Plyler (Easybugfix Volunteer)']

i = 1
tag = random.choice(tags)

urls = []

while 1:
    try:

        print ("Using Tag: "+ tag)
        url = 'https://api.stackexchange.com/2.3/questions?page='+str(i)+'&pagesize=100&order=desc&sort=activity&tagged='+tag+'&site=stackoverflow&filter=!*2b5gMKnwgyCyv_)abW2BH-puCWq.Kh)Lxytazti' 
        qlist = requests.get(url, timeout=30)
        q = qlist.json()
        if 'items' not in q.keys() or len(q['items']) < 1:
            tag = random.choice(tags)
            i = 1
            continue 
        questions = q['items']
        for j in questions:
            if j['is_answered'] and str(j['question_id']) not in posted_questions:
                for k in j['answers']:
                    if k['is_accepted']:
                        print("Publishing: " + j['title'])
                        print("* Creating Tags ")
                        tags_list = []
                        for t in j['tags']:
                            new_tag = wp.create_tag(t)
                            if 'code' in new_tag.keys() and new_tag['code'] == 'term_exists':
                                tags_list.append(new_tag['data']['term_id'])
                                print('* Tag Exist: ' + t +' | id: ' + str(new_tag['data']['term_id']))
                            else:
                                tags_list.append(new_tag['id'])
                                print('* New Tag Created Successfully: ' + t +' | id: ' + str(new_tag['id']))
                                
                        print('* Tags Created Successfully: ' + ','.join(map(lambda x:str(x), tags_list)))
                        body = """
                        <div id='dv1'></div>
                        <h2>Issue</h2>
                        <div id='dv2'></div>
                        %s
                        <div id='dv3'></div>
                        <br><div id='dv4'></div>
                        <h2>Solution</h2>
                        <div id='dv5'></div>
                        %s
                        <div id='dv6'></div>
                        <br>
                        <br>
                        <div id='dv7'></div>
                        Answered By - <a href="%s">%s</a> 
			<div id='dv8'></div>
                        Answer Checked By - <a href="https://easybugfix.com/contact-us/">%s</a> <br>
                        <div id='dv9'></div>

                        """ %( j['body'], k['body'], k['link'], k['owner']['display_name'], random.choice(checkers))


                        now = datetime.datetime.now() - datetime.timedelta(hours=6, minutes=0)

                        dt_string = now.strftime("%Y-%m-%dT%H:%M:%S")
                        print("* Creating Categories ")
                        new_cat = wp.create_category(tag)
                        
                        if 'id' in new_cat.keys():
                                cat = new_cat['id']
                                print('* New Category Created Successfully: ' + tag +' | id: ' + str(cat))
                        elif 'code' in new_cat.keys() and new_cat['code'] == 'term_exists':
                                cat = new_cat['data']['term_id']
                                print('* Category found: ' + tag +' | id: ' + str(cat))
                        else:
                            cat = 0
                                
                        post = {
                             'title'    : '[FIXED] ' + j['title'],
                             'status'   : 'publish', 
                             'content'  : body,
                             'categories': str(cat),
                             'date'   : dt_string,
                             'tags'     : ','.join(map(str,tags_list))
                        }
                        post_data = wp.post(post)

                        urls.append(post_data['link'])
                        
                        print("* Published to wordpress: " + j['title'])
                        posted_questions.append(str(j['question_id']))
                        f = open('posts.txt', 'a')
                        f.write(str(j['question_id'])+'\n')
                        f.close()
                        print("* Updated posts.txt")
                        githelper.git_push(path, "Published: " + j['title'])
                        print("* Updated git repo")
                        time.sleep(random.randint(800,1200))
                        
                        break
        i+=1
        if i > 24:
            '''print('Submitting %s urls :' % (len(urls)))
            print (index.index(urls))
            urls = []'''
            
            i = 1
            tag = random.choice(tags)
            print('Changing page :' + i +" | tag : " + tag)

            
    except Exception as e:
        print(e)
  
