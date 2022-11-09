from abc import ABC, abstractmethod
import numpy as np



class Variable:
    
    def __init__(self, data: np.ndarray) -> None:
        self.data = data
        self.grad = np.zeros_like(data)  # droot / dself
        self.shape = data.shape
        self.is_leaf = True
        self.prev = None
    
    def backward(self, grad: np.ndarray = 1.0) -> None:

        self.grad += grad
        
        # Depth-first traversal
        if not self.is_leaf:
            fn, fn_vars = self.prev[0], self.prev[1]
            # fn_vars_local_deriv = fn.jac(*fn_vars)
            fn_vars_vjp = fn.vjp(grad, self, *fn_vars)
            
            for i in range(len(fn_vars)):

                # # Chain rule
                # if len(self.shape) >= 1:
                #     fn_var_grad = fn_vars_local_deriv[i] @ self.grad 
                # else:
                #     fn_var_grad = fn_vars_local_deriv[i] * self.grad 
                fn_var_grad = fn_vars_vjp[i]
                fn_vars[i].backward(fn_var_grad)


    def __neg__(self):
        return Neg()(self)

    def __add__(self, x2):
        return Add()(self, x2)

    def __mul__(self, x2):
        return Mul()(self, x2)

    def sum(self):
        return Sum()(self)


class Function(ABC):
    
    def __call__(self, *args: Variable) -> Variable:
        y_data = self.f(*args)
        y = Variable(y_data)
        y.is_leaf = False
        y.prev = [self, args]
        return y

    @abstractmethod
    def f(self, *args: Variable) -> np.ndarray:
        ...

    @abstractmethod
    def jac(self, *args: Variable) -> list[np.ndarray]:
        # Jacobian
        ...

    @abstractmethod
    def vjp(self, grad: np.ndarray, result: Variable, *args: Variable) -> list[np.ndarray]:
        # Vector-Jacobian product
        ...


class Neg(Function):

    def f(self, x):
        return -x.data

    def jac(self, x):
        dx = np.eye(x.data.flatten().shape[0]) * (-1)
        dx = dx.reshape(x.shape + x.shape)
        return [dx]

    def vjp(self, grad, result, x):
        return [-grad]


class Sum(Function):

    def f(self, x):
        return x.data.sum()

    def jac(self, x):
        dx = np.ones_like(x.data)
        return [dx]

    def vjp(self, grad, result, x):
        return [grad]


class Add(Function):

    def f(self, x1, x2):
        return x1.data + x2.data

    def jac(self, x1, x2):
        dx1 = np.eye(x1.data.flatten().shape[0])
        dx1 = dx1.reshape(x1.shape + x1.shape)
        dx2 = np.eye(x2.data.flatten().shape[0])
        dx2 = dx2.reshape(x2.shape + x2.shape)
        return [dx1, dx2]

    def vjp(self, grad, result, x1, x2):
        return [grad, grad]


class Sub(Function):

    def f(self, x1, x2):
        return x1.data - x2.data

    def jac(self, x1, x2):
        dx1 = np.eye(x1.data.flatten().shape[0])
        dx1 = dx1.reshape(x1.shape + x1.shape)
        dx2 = np.eye(x2.data.flatten().shape[0]) * (-1)
        dx2 = dx2.reshape(x2.shape + x2.shape)
        return [dx1, dx2]

    def vjp(self, grad, result, x1, x2):
        return [grad, -grad]


class Mul(Function):

    def f(self, x1, x2):
        return x1.data * x2.data

    def jac(self, x1, x2):
        dx1 = np.diag(x2.data.flatten())
        dx1 = dx1.reshape(x2.shape + x1.shape)
        dx2 = np.diag(x1.data.flatten())
        dx2 = dx2.reshape(x1.shape + x2.shape)
        return [dx1, dx2]

    def vjp(self, grad, result, x1, x2):
        return [grad * x2.data, grad * x1.data]


class Div(Function):

    def f(self, x1, x2):
        return x1.data / x2.data

    def jac(self, x1, x2):
        dx1 = 1.0 / np.diag(x2.data.flatten())
        dx1 = dx1.reshape(x2.shape + x1.shape)
        dx2 = (-1.0 / (np.diag(x2.data.flatten()) ** 2)) * np.diag(x1.data.flatten())
        dx2 = dx2.reshape(x1.shape + x2.shape)
        return [dx1, dx2]

    def vjp(self, grad, result, x1, x2):
        return [grad * (1.0 / x2.data), grad * x1.data * (-1.0 / (x2.data**2))]


class Tanh(Function):

    def f(self, x):
        return np.tanh(x.data)

    def jac(self, x):
        dx = np.diag(np.flatten(1 - np.tanh(x.data)**2))
        return [dx]

    def vjp(self, grad, result, x):
        return [grad * (1 - np.tanh(x.data)**2)]



if __name__ == '__main__':

    
    a = Variable(np.array([1., 1.]))
    b = Variable(np.array([3., 3.]))
     
    c = a * b
    o = c.sum()
    print(o.data)

    o.backward()
    print(o.grad)
    print(c.grad)
    print(a.grad)
    print(b.grad)