class DemolitionEmissionsCalculator:
    def __init__(self):
        self.emission_factor_diesel = 2.68
        self.emission_factor_petrol = 2.31
        self.avg_car_consumption = 0.07
        self.avg_tool_consumption = {"excavator":15,"bulldozer":20,"crane":12,"truck":25}
        self.traffic_profile = {"morning_peak":0.35,"midday":0.20,"evening_peak":0.35,"night":0.10}
        self.total_daily_cars = 50000

    def estimate_cars_at_time(self, time_slot):
        if time_slot not in self.traffic_profile: 
            print("uh oh invalid time slot!")
            return 0
        return int(self.total_daily_cars*self.traffic_profile[time_slot])

    def car_emissions(self,num_cars,extra_km,fuel_type="petrol"):
        if fuel_type=="diesel":
            factor=self.emission_factor_diesel
        else:
            factor=self.emission_factor_petrol
        fuel_used = num_cars*extra_km*self.avg_car_consumption
        emissions = fuel_used*factor
        return emissions,fuel_used

    def tool_emissions(self,tools_usage):
        total_emissions=0
        total_fuel=0
        for t,h in tools_usage.items():
            if t in self.avg_tool_consumption:
                f=self.avg_tool_consumption[t]*h
                total_fuel+=f
                total_emissions+=f*self.emission_factor_diesel
        return total_emissions,total_fuel

    def daily_project_emissions(self,num_cars,extra_km,tools_usage,fuel_type="petrol"):
        c_em,c_f=self.car_emissions(num_cars,extra_km,fuel_type)
        t_em,t_f=self.tool_emissions(tools_usage)
        return {"car_emissions_kg":c_em,"tool_emissions_kg":t_em,"total_emissions_kg":c_em+t_em,
                "car_fuel_l":c_f,"tool_fuel_l":t_f,"total_fuel_l":c_f+t_f}

fuel_type="diesel"
extra_km=2.5

demolition_tools={"excavator":10,"bulldozer":6,"truck":8}
rebuild_tools={"crane":7,"truck":10}

demolition_days=14
rebuild_days=60

time_slot="morning_peak"

if __name__=="__main__":
    calc=DemolitionEmissionsCalculator()
    cars_per_day=calc.estimate_cars_at_time(time_slot)

    # demo phase
    daily_demo=calc.daily_project_emissions(cars_per_day,extra_km,demolition_tools,fuel_type)
    total_demo={}
    for k,v in daily_demo.items():
        total_demo[k]=v*demolition_days
    cars_demo_total=cars_per_day*demolition_days

    daily_rebuild=calc.daily_project_emissions(cars_per_day,extra_km,rebuild_tools,fuel_type)
    total_rebuild={}
    for k,v in daily_rebuild.items():
        total_rebuild[k]=v*rebuild_days
    cars_rebuild_total=cars_per_day*rebuild_days

    project_total={}
    for k in total_demo:
        project_total[k]=total_demo[k]+total_rebuild[k]
    cars_project_total=cars_demo_total+cars_rebuild_total

    print("==== DEMO + REBUILD EMISSIONS REPORT ====\n")
    print("Demolition phase (",demolition_days,"days):")
    print("- Cars affected per day:",cars_per_day)
    print("- Total cars affected:",cars_demo_total)
    print("- Cars (detour):",total_demo["car_emissions_kg"],"kg CO2 (",total_demo["car_fuel_l"],"L fuel)")
    print("- Tools:",total_demo["tool_emissions_kg"],"kg CO2 (",total_demo["tool_fuel_l"],"L fuel)")
    print("- TOTAL:",total_demo["total_emissions_kg"],"kg CO2\n")

    print("Rebuild phase (",rebuild_days,"days):")
    print("- Cars affected per day:",cars_per_day)
    print("- Total cars affected:",cars_rebuild_total)
    print("- Cars (detour):",total_rebuild["car_emissions_kg"],"kg CO2 (",total_rebuild["car_fuel_l"],"L fuel)")
    print("- Tools:",total_rebuild["tool_emissions_kg"],"kg CO2 (",total_rebuild["tool_fuel_l"],"L fuel)")
    print("- TOTAL:",total_rebuild["total_emissions_kg"],"kg CO2\n")

    print("=== Overall ===")
    print("- Cars affected in total:",cars_project_total)
    print("- Cars:",project_total["car_emissions_kg"],"kg CO2")
    print("- Tools:",project_total["tool_emissions_kg"],"kg CO2")
    print("- TOTAL PROJECT:",project_total["total_emissions_kg"],"kg CO2")

