import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

public class CPD {
	public static void main(String[] args) {
		double x1 = 1. / 2, x0 = 1. / 2;
		double y1 = 1. / 2, y0 = 1. / 2;

		Map<Integer, Double> cpd = new HashMap<>();
		cpd.put(0b000, 1. / 2);
		cpd.put(0b001, 1. / 2);
		cpd.put(0b010, 1. / 2);
		cpd.put(0b011, 1. / 2);
		cpd.put(0b100, 1. / 2);
		cpd.put(0b101, 1. / 2);
		cpd.put(0b110, 1. / 6);
		cpd.put(0b111, 5. / 6);

		System.out.println("x0 : " + x0 + ", y0 : " + y0);
		System.out.println("x1 : " + x1 + ", y1 : " + y1);

		Double total;
		total = 0.0;
		for (Entry<Integer, Double> entry : cpd.entrySet()) {
			total += entry.getValue();
		}
		System.out.println("Total CPD : " + total);

		Map<Integer, Double> tpd = new HashMap<>();
		tpd.put(0b000, x0 * y0 * cpd.get(0b000));
		tpd.put(0b001, x0 * y0 * cpd.get(0b001));
		tpd.put(0b010, x0 * y1 * cpd.get(0b010));
		tpd.put(0b011, x0 * y1 * cpd.get(0b011));
		tpd.put(0b100, x1 * y0 * cpd.get(0b100));
		tpd.put(0b101, x1 * y0 * cpd.get(0b101));
		tpd.put(0b110, x1 * y1 * cpd.get(0b110));
		tpd.put(0b111, x1 * y1 * cpd.get(0b111));

		total = 0.0;
		for (Entry<Integer, Double> entry : tpd.entrySet()) {
			total += entry.getValue();
		}
		System.out.println("Total TPD : " + total);

		Double temp1 = tpd.get(0b100) + tpd.get(0b101) + tpd.get(0b110) + tpd.get(0b111);
		System.out.println("x1 : " + temp1);
		Double temp2 = tpd.get(0b010) + tpd.get(0b011) + tpd.get(0b110) + tpd.get(0b111);
		System.out.println("y1 : " + temp2);

		Double z0 = tpd.get(0b000) + tpd.get(0b010) + tpd.get(0b100) + tpd.get(0b110);
		Double z1 = tpd.get(0b001) + tpd.get(0b011) + tpd.get(0b101) + tpd.get(0b111);

		System.out.println("z0 : " + z0 + ", z1 : " + z1);

		// Part 1
		{
			System.out.println("-------------------------------------------------------------------------");
			// P(z1 | x1) > P(z1)
			Double var1 = (tpd.get(0b101) + tpd.get(0b111)) / x1;
			System.out.println(" P(z1 | x1) [" + var1 + "] > P(z1) [" + z1 + "] " + (var1 > z1));

			// P(z1 | x1) > P(z1)
			Double var2 = (tpd.get(0b011) + tpd.get(0b111)) / x1;
			System.out.println(" P(z1 | y1) [" + var2 + "] > P(z1) [" + z1 + "] " + (var2 > z1));
		}

		// Part 2
		{
			System.out.println("-------------------------------------------------------------------------");
			// P(x1 | z1) < P(x1 | y1, z1)
			Double var1 = (tpd.get(0b101) + tpd.get(0b111)) / z1;
			Double var2 = (tpd.get(0b111)) / (tpd.get(0b011) + tpd.get(0b111));

			System.out.println(" P(x1 | z1) [" + var1 + "] < P(x1 | y1, z1) [" + var2 + "] " + (var1 < var2));

			// P(y1 | z1) < P(y1 | x1, z1)
			Double var3 = (tpd.get(0b011) + tpd.get(0b111)) / z1;
			Double var4 = (tpd.get(0b111)) / (tpd.get(0b101) + tpd.get(0b111));
			System.out.println(" P(x1 | z1) [" + var3 + "] < P(x1 | y1, z1) [" + var4 + "]" + (var3 < var4));
		}
	}
}
