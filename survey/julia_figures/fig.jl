using Plots
using Distributions

# Goal is to plot the pdf of 3 different distributions to compare the risk of each
# all three distributions have the same mean, but different variances

# Define the distributions
d1 = Normal(0, 1)
d2 = Normal(0, 2)
d3 = Cauchy(0, 0.5)

# Plot all three
@show mean(d1)
plot(pdf(d1, -5:0.01:5), label="", lw=2, color=:purple, fillrange=0, fillalpha=0.3, fillcolor=:purple)
savefig("normal.pdf")
@show mean(d2)
plot(pdf(d2, -5:0.01:5), label="", lw=2, color=:green, fillrange=0, fillalpha=0.3, fillcolor=:green)
savefig("normal_wide.pdf")
@show mean(d3)
plot(pdf(d3, -5:0.01:5), label="", lw=2, color=:blue, fillrange=0, fillalpha=0.3, fillcolor=:blue)
savefig("cauchy.pdf")
