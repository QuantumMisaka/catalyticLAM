import os
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
def extract_energies(oszicar_path):
    energies = []
    if os.path.exists(oszicar_path):
        with open(oszicar_path, 'r') as file:
            for line in file:
                if 'E0=' in line:
                    energy = float(line.split()[4])
                    energies.append(energy)
    return energies

def extract_forces(outcar_path):
    forces = []
    if os.path.exists(outcar_path):
        with open(outcar_path, 'r') as file:
            for line in file:
                if 'RMS' in line:
                    force = float(line.split()[4])
                    forces.append(force)
    return forces

def main():
    iterations = 10  # Default number of iterations
    all_energies = []
    all_forces = []
    steps = []

    for i in range(1, iterations + 1):
        folder = f'opt{i}'
        oszicar_path = os.path.join(folder, 'OSZICAR')
        outcar_path = os.path.join(folder, 'OUTCAR')

        energies = extract_energies(oszicar_path)
        forces = extract_forces(outcar_path)

        all_energies.extend(energies)
        all_forces.extend(forces)
        steps.extend([i] * len(energies))  # Assuming each energy corresponds to a single step

    # Include the final optimization folder
    final_folder = 'optfinal'
    final_oszicar_path = os.path.join(final_folder, 'OSZICAR')
    final_outcar_path = os.path.join(final_folder, 'OUTCAR')

    final_energies = extract_energies(final_oszicar_path)
    final_forces = extract_forces(final_outcar_path)

    all_energies.extend(final_energies)
    all_forces.extend(final_forces)
    steps.extend(['final'] * len(final_energies))  # Mark the final steps

    # Extract data from the optall folder for comparison
    all_folder = 'optall'
    all_oszicar_path = os.path.join(all_folder, 'OSZICAR')
    all_outcar_path = os.path.join(all_folder, 'OUTCAR')

    all_comparison_energies = extract_energies(all_oszicar_path)
    all_comparison_forces = extract_forces(all_outcar_path)
    all_comparison_steps = list(range(len(all_comparison_energies)))

    # Plotting the energy change
    plt.figure()
    plt.plot(range(len(all_energies)), all_energies, marker='o', linestyle='-', color='b', label='opt DP+DFT iterations')
    plt.plot(all_comparison_steps, all_comparison_energies, marker='x', linestyle='--', color='g', label='opt DFT')
    plt.xlabel('Step')
    plt.ylabel('Energy (eV)')
    plt.title('Energy Change Over Steps')
    plt.legend()
    plt.grid(True)
    # Add inset for energy plot with specified xlim and ylim
    ax_inset = inset_axes(plt.gca(), width="50%", height="50%", loc="right")
    ax_inset.plot(range(len(all_energies)), all_energies, 'bo-')
    ax_inset.plot(all_comparison_steps, all_comparison_energies, 'gx--')
    ax_inset.set_xlim(0, len(all_energies))  # Specify xlim for inset
    energy_min, energy_max = min(all_energies), max(all_energies)
    margin = (energy_max - energy_min) * 0.1  # 10% margin
    ax_inset.set_ylim(energy_min - margin, energy_max + 0.5*margin)
    ax_inset.tick_params(axis='both', which='major', labelsize=8)  # Adjust tick label size
    ax_inset.grid(True)
    plt.savefig('opt_energy_change_comparison.png')
    plt.show()

    # Plotting the max force change
    plt.figure()
    plt.plot(range(len(all_forces)), all_forces, marker='o', linestyle='-', color='r', label='opt DP+DFT iterations')
    plt.plot(all_comparison_steps, all_comparison_forces, marker='x', linestyle='--', color='m', label='opt DFT')
    plt.xlabel('Step')
    plt.ylabel('Max Force (eV/Å)')
    plt.title('Max Force Change Over Steps')
    plt.legend()
    plt.grid(True)
    # Add inset for force plot with specified xlim and ylim
    ax_inset = inset_axes(plt.gca(), width="50%", height="50%", loc="right")
    ax_inset.plot(range(len(all_forces)), all_forces, 'ro-')
    ax_inset.plot(all_comparison_steps, all_comparison_forces, 'mx--')
    ax_inset.set_xlim(0, len(all_forces))  # Specify xlim for inset
    force_min, force_max = min(all_forces), max(all_forces)
    margin = (force_max - force_min) * 0.1  # 10% margin
    ax_inset.set_ylim(force_min - margin, force_max + 0.5*margin)
    ax_inset.tick_params(axis='both', which='major', labelsize=8)  # Adjust tick label size
    ax_inset.grid(True)

    plt.savefig('opt_force_change_comparison.png')
    plt.show()

if __name__ == '__main__':
    main()
