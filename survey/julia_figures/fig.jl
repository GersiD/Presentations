using Plots
using Distributions

# Goal is to plot the pdf of 3 different distributions to compare the risk of each
# all three distributions have the same mean, but different variances

# Define the distributions
d1 = Normal(0, 1)
m1 = mean(d1)
d2 = Normal(0, 2)
m2 = mean(d2)
d3 = Laplace(0, 1)
m3 = mean(d3)

# Plot all three
# Vertical lines at the mean
range = -5:0.01:5
plot(range, pdf(d1, range), label="", lw=2, color=:purple, fillrange=0, fillalpha=0.3, fillcolor=:purple)
vline!([m1], label="", color=:purple, lw=2)
savefig("normal.pdf")
plot(range, pdf(d2, range), label="", lw=2, color=:green, fillrange=0, fillalpha=0.3, fillcolor=:green)
vline!([m2], label="", color=:green, lw=2)
savefig("normal_wide.pdf")
plot(range, pdf(d3, range), label="", lw=2, color=:blue, fillrange=0, fillalpha=0.3, fillcolor=:blue)
vline!([m3], label="", color=:blue, lw=2)
savefig("laplace.pdf")
