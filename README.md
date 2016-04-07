# IPv4 CIDR Address Allocation
A utility to manage allocating and deallocating CIDR networks.

## Problem Statement
CIDR address allocation is a complex problem. Some might think it is very close to the memory allocation problem. But
it's more complex than that because of recursively dividing the address space into two till a best fit is found. 

For a clearer view of the problem, let's say you have an apple and you can cut a unit in half only. So if a friend asked
for 1/4th slice, you would have to cut it twice. This would leave you with two slices, a 1/4th slice and a 1/2 slice. If
    another friend now asks for a 3/4th piece of apple, you can't allocate him that because you need to give him a
    single piece only. 

Let's make things clear with an example. Let's say you have a network 10.10.0.0/20. Now, the Computer Science department
posts a requirement of a 1000 host machines. This means that the network you'll allocate will be /22 subnet from the
given network. To get to that, you divide the network into 2 parts and you get a /21 network. Now you pick the left one (for ease of policy) and divide it into 2 again and you get a /22 network to allocate. 

## Setup
### Linux
Make sure you have Python 2.7 installed on your machine. Install the *bokeh* and *ipaddr* packages:

> sudo pip install bokeh
> sudo pip install ipaddr

### Windows
While installing Python, make sure you choose the "Add Python.exe to PATH" option. Open the command prompt and install
*bokeh* and *ipaddr* modules for Python

> python -m pip install bokeh
> python -m pip install ipaddr

## Usage
- Start the script in interactive mode
```
python -i ipam.py
```
- Initialize your network address space
```python
ipam = IPAM("10.10.0.0/24")
```
- Allocate subnets according to your size requirements
NOTE: Subnets allocation policy is left-first. 
```python
ipam.add(1000)
ipam.add(100)
ipam.add(250)
ipam.add(60)
```
- View allocations
```python
ipam.plot()
```
## TODO:
- Ability to delete subnets
- Other subnet allocation policy
