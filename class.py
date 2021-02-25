#!/usr/bin/python3
# HS 08Dec21
# Harpreet starting with class
## https://realpython.com/python3-object-oriented-programming/

class VirtualServer:
  # Class attribute
  # They must always be assigned an initial value
  type = 'Standard'
  
  def __init__(self, name, vip, port):
    self.name = name # Instance attribute
    self.vip = vip
    self.port = port
  
  # Dunder method. It begin and end with double underscores
  def __str__(self):
    return f"{self.name} VIP is {self.vip}:{self.port}"
  
  # Instance method
  def description(self):
    return f"{self.name} VIP is {self.vip}:{self.port}"

if __name__ = "__main__":
  sports_vs = VirtualServer("sports_vs", "147.188.10.11", 443)
  blog_vs = VirtualServer("blog_vs", "147.188.10.10", 443)
