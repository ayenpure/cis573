import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

public class CPD2 {
	public static void main(String[] args) {
		double x1 = 1. / 10000, x0 = 1 - x1;
		double y1 = 1. / 10000, y0 = 1 - y1;

		Map<Integer, Double> scpd = new HashMap<>();
		scpd.put(0b000, 1.);
		scpd.put(0b001, 0.);
		scpd.put(0b010, .5);
		scpd.put(0b011, .5);
		scpd.put(0b100, .5);
		scpd.put(0b101, .5);
		scpd.put(0b110, .25);
		scpd.put(0b111, .75);

		System.out.println("x0 : " + x0 + ", y0 : " + y0);
		System.out.println("x1 : " + x1 + ", y1 : " + y1);

		Double total;
		total = 0.0;
		for (Entry<Integer, Double> entry : scpd.entrySet()) {
			total += entry.getValue();
		}
		System.out.println("Total SCPD : " + total);

		Map<Integer, Double> dcpd = new HashMap<>();
		dcpd.put(0b000, 1.);
		dcpd.put(0b001, 0.);
		dcpd.put(0b010, .5);
		dcpd.put(0b011, .5);
		dcpd.put(0b100, .5);
		dcpd.put(0b101, .5);
		dcpd.put(0b110, .25);
		dcpd.put(0b111, .75);

		total = 0.0;
		for (Entry<Integer, Double> entry : dcpd.entrySet()) {
			total += entry.getValue();
		}
		System.out.println("Total DCPD : " + total);

		Map<Integer, Double> tpd = new HashMap<>();
		tpd.put(0b0000, x0 * y0 * scpd.get(0b000) * dcpd.get(0b000));
		tpd.put(0b1000, x1 * y0 * scpd.get(0b100) * dcpd.get(0b100));
		tpd.put(0b0100, x0 * y1 * scpd.get(0b010) * dcpd.get(0b010));
		tpd.put(0b1100, x1 * y1 * scpd.get(0b110) * dcpd.get(0b110));

		tpd.put(0b0010, x0 * y0 * scpd.get(0b001) * dcpd.get(0b000));
		tpd.put(0b1010, x1 * y0 * scpd.get(0b101) * dcpd.get(0b100));
		tpd.put(0b0110, x0 * y1 * scpd.get(0b011) * dcpd.get(0b010));
		tpd.put(0b1110, x1 * y1 * scpd.get(0b111) * dcpd.get(0b110));

		tpd.put(0b0001, x0 * y0 * scpd.get(0b000) * dcpd.get(0b001));
		tpd.put(0b1001, x1 * y0 * scpd.get(0b100) * dcpd.get(0b101));
		tpd.put(0b0101, x0 * y1 * scpd.get(0b010) * dcpd.get(0b011));
		tpd.put(0b1101, x1 * y1 * scpd.get(0b110) * dcpd.get(0b111));

		tpd.put(0b0011, x0 * y0 * scpd.get(0b001) * dcpd.get(0b001));
		tpd.put(0b1011, x1 * y0 * scpd.get(0b101) * dcpd.get(0b101));
		tpd.put(0b0111, x0 * y1 * scpd.get(0b011) * dcpd.get(0b011));
		tpd.put(0b1111, x1 * y1 * scpd.get(0b111) * dcpd.get(0b111));

		total = 0.0;
		for (Entry<Integer, Double> entry : tpd.entrySet()) {
			total += entry.getValue();
		}
		System.out.println("Total TPD : " + total);

		{
			// P(m1 | f1, s1) = P(m1, f1, s1, d0) + P(m1, f1, s1, d1) / P(m0, f1, s1, d0) +
			// P(m0, f1, s1, d1) + P(m1, f1, s1, d0) + P(m1, f1, s1, d1)
			Double var1 = (tpd.get(0b1110) + tpd.get(0b1111))
					/ (tpd.get(0b0110) + tpd.get(0b0111) + tpd.get(0b1110) + tpd.get(0b1111));
			// P (m1 | s1)
			Double var2 = (tpd.get(0b1010) + tpd.get(0b1110) + tpd.get(0b1011) + tpd.get(0b1111))
					/ (tpd.get(0b0010) + tpd.get(0b0110) + tpd.get(0b1010) + tpd.get(0b1110) + tpd.get(0b0011)
							+ tpd.get(0b0111) + tpd.get(0b1011) + tpd.get(0b1111));
			System.out.println("P(m1 | f1, s1) : " + var1);
			System.out.println("P (m1 | s1) : " + var2);
		}

		{
			// P(s1, d1)
			Double var1 = tpd.get(0b0011) + tpd.get(0b0111) + tpd.get(0b1011) + tpd.get(0b1111);

			// P(s1)
			Double var2 = tpd.get(0b0010) + tpd.get(0b0110) + tpd.get(0b1010) + tpd.get(0b1110) + tpd.get(0b0011)
					+ tpd.get(0b0111) + tpd.get(0b1011) + tpd.get(0b1111);

			// P(d1)
			Double var3 = tpd.get(0b0001) + tpd.get(0b0011) + tpd.get(0b0101) + tpd.get(0b0111) + tpd.get(0b1001)
					+ tpd.get(0b1011) + tpd.get(0b1101) + tpd.get(0b1111);

			System.out.println("P(s1, d1) : " + var1);
			System.out.println("P(s1)*P(d1) : " + var2 * var3);
		}
	}
}
