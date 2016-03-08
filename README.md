# IP Address Management Tool
A utility to manage IP addresses. Mostly allocating and deallocating CIDR networks.

## Problem
CIDR address allocation is a complex problem. Some might think it is very close to the memory allocation problem. But
it's more complex than that because of recursively dividing the address space into two till a best fit is found. 

For a clearer view of the problem, let's say you have an apple and you can cut a unit in half only. So if a friend asked
for 1/4th slice, you would have to cut it twice. This would leave you with two slices, a 1/4th slice and a 1/2 slice. If
    another friend now asks for a 3/4th piece of apple, you can't allocate him that because you need to give him a
    single piece only. 

Let's make things clear with an example. Let's say you have a network 10.10.0.0/20. Now, the Computer Science department
posts a requirement of a 1000 host machines. This means that the network you'll allocate will be /22 subnet from the
given network. To get to that, you divide the network into 2 parts and you get a /21 network. Now you pick the left one
(for ease of policy) and divide it into 2 again and you get a /22 network to allocate. After this tiresome task, your
address space looks as follows:

------------------------

----|10.10.0.0/22 

------------------------
    
----|10.10.4.0/22 free
    
------------------------
  
  
  
--|10.10.8.0/21 free
  
  
  
------------------------


## Usage
- Start the script in interactive mode
```
python -i ipam.py
```
- Initialize your network address space
```python
ipam = IPAM("10.10.0.0/24")
```
- Allocate subnets
```python
ipam.add(1000)
ipam.add(100)
ipam.add(250)
ipam.add(60)
```
- View allocations
```python
ipam.show()
```
