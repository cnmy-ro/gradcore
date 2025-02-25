import numpy as np
import nabla
from nabla import Tensor
import torch


def test_mul():
	a = Tensor(np.ones((3,3,3))*2, requires_grad=True)
	b = Tensor(np.ones((3,3,3))*4, requires_grad=True)
	c = a * b
	l = c.sum()
	l.backward()
	print(c.grad)
	print(a.grad)
	print(b.grad)

def test_dot():
	a = Tensor(np.ones((3,4))*2, requires_grad=True)
	b = Tensor(np.ones((4,2))*4, requires_grad=True)
	c = a.dot(b)
	l = c.sum()
	l.backward()
	print(c.grad)
	print(a.grad)
	print(b.grad)

def test_tensoroverwrite():
	a = Tensor(np.ones((4,1))*3, requires_grad=True)
	b = Tensor(np.ones((4,1)), requires_grad=True)
	a = a * b
	a = a.sum()
	a.backward()
	print(a.grad)
	print(b.grad)

def test_dagviz():
	a = Tensor(np.ones((4,1))*3, requires_grad=True)
	b = Tensor(np.ones((4,1)), requires_grad=True)
	c = Tensor(np.array([2]), requires_grad=True)
	d = a * b
	e = d.sum()	
	f = e * c
	nabla.show_dag(f, view_img=True)

def test_shapeops():
	a = Tensor(np.ones((4,3))*3, requires_grad=True)
	print(a.shape)
	# b = a.unsqueeze(dim=0).unsqueeze(dim=0).unsqueeze(dim=0)
	# print(b.shape)
	# c = b.squeeze()
	# print(c.shape)
	# d = c.sum()
	# d.backward()
	# print(a.grad)

	# e = a.slice(dims=[0, 1], ranges=[[0,2], [1,3]])
	# print(e.shape)
	# e.sum().backward()
	# print(a.grad)

	# b = Tensor(np.ones((4,3))*2, requires_grad=True)
	# c = Tensor(np.ones((4,3))*4, requires_grad=True)
	# d = nabla.stack([a,b,c], dim=0)
	# print(c.shape)
	# d = d.sum()
	# nabla.show_dag(d, view_img=True)
	# d.backward(grad=np.ones_like(d.data))
	# print(a.grad)

	# b = Tensor(np.ones((4,3))*2, requires_grad=True).unsqueeze(1)
	# c = Tensor(np.ones((4,3))*4, requires_grad=True).unsqueeze(1)
	# print(b.shape)
	# d = nabla.cat([b,c], dim=1)
	# d = d.sum()
	# # nabla.show_dag(d, view_img=True)
	# d.backward(grad=np.ones_like(d.data))
	# print(b.grad)

	print(a[1:3, :])


def test_conv():
	print("nabla:")
	a = Tensor(np.arange(0,8).astype(float), requires_grad=True)
	b = Tensor(np.array([-1., 0, 0., 1.]), requires_grad=True)
	c = nabla.conv1d(a,b)
	print(a)
	print(b)
	print(c)
	d = c.sum()
	d.backward(grad=np.array([1.]))
	print(a.grad)
	print(b.grad)
	# nabla.show_dag(d)

	print()

	print("torch:")
	a = torch.arange(0.,8., dtype=torch.float32, requires_grad=True)
	b = torch.tensor(np.array([-1., 0., 0. ,1.]), dtype=torch.float32, requires_grad=True)
	c = torch.conv1d(a.unsqueeze(0).unsqueeze(0), b.unsqueeze(0).unsqueeze(0))
	print(a)
	print(b)
	print(c)
	d = c.sum()
	d.backward()
	print(a.grad)
	print(b.grad)

def test_dimsum():
	print('nabla:')
	a = Tensor(np.ones((4,3)), requires_grad=True)
	b = a.mean(dim=[0])
	print(b)
	c = b.sum()
	print(c)
	c.backward()
	print(a.grad)

	print()

	print('torch:')
	a = torch.ones((4,3), requires_grad=True)
	b = a.mean(dim=[0])
	print(b)
	c = b.sum()
	print(c)
	c.backward()
	print(a.grad)

# test_dot()
# test_tensoroverwrite()
# test_dagviz()
# test_shapeops()
# test_conv()
test_dimsum()