from flask import Flask, render_template, request, jsonify
import datetime
import random
import requests
import os

app = Flask(__name__, static_folder='.', static_url_path='')

# Your API Keys
OPENWEATHER_KEY = "7e6b9c36933b6082d00de55fa969e66d"
NEWSAPI_KEY = "0431d5a730824303ab47955cde1eca54"

class LucaAssistant:
    def __init__(self):
        self.name = "Luca"
        
    def process_command(self, command):
        command = command.lower().strip()
        
        # Check if command contains "luca"
        if "luca" not in command:
            return {
                "success": False,
                "response": "Please start your command with 'Luca'",
                "shouldSpeak": True
            }
        
        # Remove "luca" and clean
        command = command.replace("luca", "").strip()
        
        # Dictionary of command handlers
        handlers = {
            "time": self.get_time,
            "date": self.get_date,
            "joke": self.tell_joke,
            "weather": self.get_weather,
            "news": self.get_news,
            "search": self.search_web,
            "open": self.open_website,
            "calculate": self.calculate,
            "note": self.take_note,
            "reminder": self.set_reminder,
            "help": self.show_help
        }
        
        # Find and execute handler
        for key, handler in handlers.items():
            if key in command:
                if key == "weather":
                    # Extract city for weather
                    city = "New York"
                    if "in" in command:
                        city = command.split("in")[-1].strip()
                    return handler(city)
                elif key == "search":
                    query = command.replace("search", "").replace("for", "").strip()
                    return handler(query)
                elif key == "open":
                    site = command.replace("open", "").strip()
                    return handler(site)
                elif key == "calculate":
                    expr = command.replace("calculate", "").strip()
                    return handler(expr)
                elif key == "note":
                    text = command.replace("note", "").replace("take", "").strip()
                    return handler(text)
                elif key == "reminder":
                    text = command.replace("reminder", "").replace("set", "").strip()
                    return handler(text)
                else:
                    return handler()
        
        # If no handler matched
        return {
            "success": True,
            "response": f"I heard: '{command}'. Try saying 'Luca help' for available commands.",
            "shouldSpeak": True
        }
    
    def get_time(self):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return {
            "success": True,
            "response": f"The time is {current_time}",
            "shouldSpeak": True
        }
    
    def get_date(self):
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        return {
            "success": True,
            "response": f"Today is {current_date}",
            "shouldSpeak": True
        }
    
    def tell_joke(self):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "What do you call fake spaghetti? An impasta!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why don't eggs tell jokes? They'd crack each other up!"
        ]
        joke = random.choice(jokes)
        return {
            "success": True,
            "response": joke,
            "shouldSpeak": True
        }
    
    def get_weather(self, city="New York"):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if data['cod'] == 200:
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                return {
                    "success": True,
                    "response": f"The weather in {city} is {temp}°C with {description}",
                    "shouldSpeak": True
                }
            else:
                return {
                    "success": False,
                    "response": f"Could not get weather for {city}",
                    "shouldSpeak": True
                }
        except Exception as e:
            return {
                "success": False,
                "response": "I'm having trouble getting the weather information.",
                "shouldSpeak": True
            }
    
    def get_news(self):
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWSAPI_KEY}"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if data['status'] == 'ok':
                headlines = [article['title'] for article in data['articles'][:3]]
                news_text = "Here are the top news headlines: "
                news_text += ". ".join(headlines)
                return {
                    "success": True,
                    "response": news_text,
                    "shouldSpeak": True
                }
            else:
                return {
                    "success": False,
                    "response": "I couldn't fetch the news right now.",
                    "shouldSpeak": True
                }
        except:
            return {
                "success": False,
                "response": "I'm having trouble getting the news.",
                "shouldSpeak": True
            }
    
    def search_web(self, query):
        if query:
            return {
                "success": True,
                "response": f"Searching for {query} on Google",
                "shouldSpeak": True,
                "action": "search",
                "query": query
            }
        else:
            return {
                "success": False,
                "response": "What would you like me to search for?",
                "shouldSpeak": True
            }
    
    def open_website(self, site):
        sites = {
            "youtube": "https://www.youtube.com",
            "github": "https://github.com",
            "gmail": "https://mail.google.com",
            "google": "https://www.google.com"
        }
        
        if site in sites:
            return {
                "success": True,
                "response": f"Opening {site}",
                "shouldSpeak": True,
                "action": "open",
                "url": sites[site]
            }
        else:
            return {
                "success": False,
                "response": f"I don't know how to open {site}",
                "shouldSpeak": True
            }
    
    def calculate(self, expression):
        try:
            # Safe calculation
            allowed_chars = set('0123456789+-*/.() ')
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                return {
                    "success": True,
                    "response": f"The result is {result}",
                    "shouldSpeak": True
                }
            else:
                raise ValueError("Unsafe characters")
        except:
            return {
                "success": False,
                "response": "I couldn't calculate that.",
                "shouldSpeak": True
            }
    
    def take_note(self, text):
        if text:
            return {
                "success": True,
                "response": f"Note saved: {text}",
                "shouldSpeak": True
            }
        else:
            return {
                "success": False,
                "response": "What would you like me to note down?",
                "shouldSpeak": True
            }
    
    def set_reminder(self, text):
        if text:
            return {
                "success": True,
                "response": f"Reminder set: {text}",
                "shouldSpeak": True
            }
        else:
            return {
                "success": False,
                "response": "What should I remind you about?",
                "shouldSpeak": True
            }
    
    def show_help(self):
        help_text = """
        I can help you with:
        • Time and date information
        • Weather updates
        • News headlines
        • Web searching
        • Opening websites
        • Calculations
        • Taking notes
        • Setting reminders
        • Telling jokes
        
        Just say "Luca" followed by what you need!
        """
        return {
            "success": True,
            "response": help_text,
            "shouldSpeak": True
        }

# Initialize assistant
assistant = LucaAssistant()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/command', methods=['POST'])
def handle_command():
    try:
        data = request.json
        command = data.get('command', '').strip()
        
        if not command:
            return jsonify({
                "success": False,
                "error": "No command provided",
                "shouldSpeak": True
            })
        
        # Process command
        result = assistant.process_command(command)
        
        # If there's an action (like open website), add it
        if 'action' in result:
            if result['action'] == 'search' and 'query' in result:
                # In a real app, you'd open the URL
                pass
            elif result['action'] == 'open' and 'url' in result:
                # In a real app, you'd open the URL
                pass
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "shouldSpeak": True
        })

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        "status": "online",
        "assistant": "Luca",
        "features": ["voice", "weather", "news", "calculations"]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
