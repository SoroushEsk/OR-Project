from minizinc import Solver, Model, Instance
solver = Solver.lookup("cbc")
model = Model("./portfolio.mzn")
model.add_file("./portfolio.dzn")
model.add_string(f"constraint x[1] <= 2")
instance = Instance(solver, model)
result = instance.solve()
print(result)